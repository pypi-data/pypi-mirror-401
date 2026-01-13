import http.server,ssl,json,base64,socket,threading,os,socketserver

MODEL_DIR = os.environ.get("DEARNING_MODEL_DIR", "dm_models")
if not os.path.exists(MODEL_DIR): os.makedirs(MODEL_DIR, exist_ok=True)
DEFAULT_PASSWORD = os.environ.get("DEARNING_PASSWORD", "dearning_secure")
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = int(os.environ.get("DEARNING_PORT", "8443"))
_SERVICE_CONTROL={}
_SERVICE_LOCK = threading.Lock()

def DGS(cert_dir: str, force_path_required=True):
    '''still experimental'''
    if force_path_required and not cert_dir: raise ValueError("Path folder sertifikat wajib diisi!")
    cert_dir = os.path.abspath(cert_dir)
    cert_path = os.path.join(cert_dir, "server.crt")
    key_path = os.path.join(cert_dir, "server.key")
    if not os.path.exists(MODEL_DIR): os.makedirs(MODEL_DIR)
    def _hash_file(path):
        import hashlib
        if not os.path.exists(path): return None
        try:
            with open(path, "rb") as f: return hashlib.sha256(f.read()).hexdigest()
        except Exception: return None
    old_cert_hash = _hash_file(cert_path)
    old_key_hash  = _hash_file(key_path)
    already_exists = old_cert_hash is not None and old_key_hash is not None
    def generate():
        import subprocess
        p = subprocess.Popen([
            "openssl", "req", "-x509", "-nodes", "-days", "365",
            "-newkey", "rsa:2048",
            "-keyout", key_path,
            "-out", cert_path,
            "-subj", "/CN=localhost"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        return p.returncode == 0
    if already_exists:
        print("[dearning] Certificate found. Checking authenticity...")
        return cert_path, key_path
    for attempt in range(1, 4):
        print("[dearning] Creating certificate (trial {})...".format(attempt))
        if generate():
            print("[dearning] Certificate successfully created in {}".format(cert_dir))
            break
        else: print("[dearning] Failed… try again…")
    if not os.path.exists(cert_path) or not os.path.exists(key_path): raise RuntimeError("Failed to create certificate after 3 attempts.")
    new_cert_hash = _hash_file(cert_path)
    new_key_hash = _hash_file(key_path)
    if already_exists and (old_cert_hash != new_cert_hash or old_key_hash != new_key_hash): print("[dearning] Certificate updated (different content).")
    elif already_exists: print("[dearning] The certificate has not changed.")
    return cert_path, key_path

_MAX_CACHE_BYTES = 2 * 1024 * 1024
_model_cache = {}

class DearningHandler(http.server.BaseHTTPRequestHandler):
    __slots__ = ("headers","rfile","wfile","command","path","server")
    protocol_version = "HTTP/1.1"
    server_version = "DearningServer/1.0" 
    def _read_json(self):
        try:
            cl = self.headers.get("Content-Length")
            if cl is None: return None
            try:length = int(cl)
            except ValueError: return None
            if length <= 0 or length > 10 * 1048576:
                self.send_error(413, "Payload Too Large")
                return None
            try: self.connection.settimeout(10)
            except Exception: pass
            raw = self.rfile.read(length)
            if not raw or len(raw) != length: return None
            return json.loads(raw.decode("utf-8"))
        except Exception: return None
    def _send_json(self, code, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def do_POST(self):
        data = self._read_json()
        if not data: return self._send_json(400, {"error": "invalid json"})
        password = data.get("password")
        if password != getattr(self.server, "cloud_password", DEFAULT_PASSWORD): return self._send_json(403, {"error": "invalid password"})
        if self.path == "/import_model": return self._handle_import_model(data)
        elif self.path == "/load_model": return self._handle_load_model(data)
        return self._send_json(404, {"error": "unknown endpoint"})
    def _handle_import_model(self, data):
        saved = []
        if "files" in data:
            for f in data["files"]:
                fname = f.get("filename")
                content_b64 = f.get("content_b64")
                if not fname or not content_b64: continue
                try: raw = base64.b64decode(content_b64)
                except Exception:
                    print("[dearning] invalid base64 for", fname)
                    continue
                safe_name = os.path.basename(fname)
                path = os.path.join(MODEL_DIR, safe_name)
                tmp = os.path.splitext(path)[0] + ".tmp"
                with open(tmp, "wb") as out: out.write(raw)
                os.replace(tmp, path)
                saved.append(safe_name)
                if os.path.getsize(path) <= _MAX_CACHE_BYTES: _model_cache[safe_name] = raw
            return self._send_json(200, {"status": "imported", "files": saved})
        else: # single file fallback
            fname = data.get("filename")
            content_b64 = data.get("content_b64")
            if not fname or not content_b64: return self._send_json(400, {"error": "missing filename or content"})
            try: raw = base64.b64decode(content_b64)
            except Exception: return self._send_json(400, {"error": "invalid base64 content"})
            safe_name = os.path.basename(fname)
            path = os.path.join(MODEL_DIR, safe_name)
            tmp = os.path.splitext(path)[0] + ".tmp"
            with open(tmp, "wb") as fh: fh.write(raw)
            os.replace(tmp, path)
            if os.path.getsize(path) <= _MAX_CACHE_BYTES: _model_cache[safe_name] = raw
            return self._send_json(200, {"status": "imported", "model": safe_name, "size": os.path.getsize(path)})
    def _handle_load_model(self, data):
        files = []
        if "filenames" in data:
            files = []
            for fname in data.get("filenames") or []:
                if not fname: continue
                safe_name = os.path.basename(fname)
                path = os.path.join(MODEL_DIR, safe_name)
                # if file does NOT exist -> mark error and continue
                if not os.path.exists(path):
                    files.append({"filename": safe_name, "error": "not found"})
                    continue
                try:
                    if safe_name in _model_cache: content = _model_cache[safe_name]
                    else:
                        with open(path, "rb") as fh: content = fh.read()
                        if len(content) <= _MAX_CACHE_BYTES: _model_cache[safe_name] = content
                    b64 = base64.b64encode(content).decode("ascii")
                    files.append({"filename": safe_name, "content_b64": b64})
                except Exception as e:
                    print("[dearning] failed to read file {}: {}".format(safe_name,e))
                    files.append({"filename": safe_name, "error": "read failed"})
            return self._send_json(200, {"status": "ok", "files": files})
        # single file fallback backwards compatible
        fname = data.get("filename")
        if not fname: return self._send_json(400, {"error": "missing filename"})
        safe_name = os.path.basename(fname)
        path = os.path.join(MODEL_DIR, safe_name)
        if not os.path.exists(path): return self._send_json(404, {"error": "not found"})
        try:
            if safe_name in _model_cache: content = _model_cache[safe_name]
            else:
                with open(path, "rb") as fh: content = fh.read()
                if len(content) <= _MAX_CACHE_BYTES: _model_cache[safe_name] = content
            b64 = base64.b64encode(content).decode("ascii")
            return self._send_json(200, {"status": "ok", "files": [{"filename": safe_name, "content_b64": b64}]})
        except Exception as e:
            print("[dearning] failed to read file {}: {}".format(safe_name,e))
            return self._send_json(500, {"error": "read failed"})

    def log_message(self, format: str, *args) -> None: return

class ThreadedHTTPSServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    cloud_password = DEFAULT_PASSWORD

def run_server(host=DEFAULT_HOST, port=DEFAULT_PORT, password=DEFAULT_PASSWORD, sslc=False, mode="internal", threaded=True, daemon=True):
    '''This function is used to make a simple server or network.
    
        example:
        >>> run_server(host="127.0.0.1", port=8080, password=4321, sslc=False, mode="internal", threaded=True, daemon=True)'''
    def _detect_server_mode():
        with _SERVICE_LOCK: info = _SERVICE_CONTROL.get("server_info", {})
        return info.get("mode"), info.get("host"), info.get("port"), info.get("sslc")

    def _start():
        if mode == "cable": # Mode kabel USB tethering
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
            finally: s.close()
            host_local = local_ip
            sslc_local = False
            print("[dearning] Wired Mode is active at http://{}:{}".format(host_local,port))
        elif mode == "wifi": # Mode WiFi
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
            finally: s.close()
            host_local = local_ip
            sslc_local = False
            print("[dearning] WiFi mode is active at http://{}:{}".format(host_local,port))
        elif mode == "mesh":
            mesh_file = os.path.join(MODEL_DIR, "mesh_peers.json")
            peers = []
            try:
                if os.path.exists(mesh_file):
                    with open(mesh_file, "r") as f: peers = json.loads(f.read() or "[]")
                else:
                    with open(mesh_file, "w") as f: f.write("[]")
            except Exception: peers = []
            peers = list({p for p in peers if isinstance(p, str)})
            print("[mesh] Active peers: {}".format(len(peers)))
            sslc_local = False
            host_local = host
        else: # Mode internal
            host_local = host
            sslc_local = sslc
        httpd = ThreadedHTTPSServer((host_local, port), DearningHandler)
        httpd.cloud_password = password
        # publish httpd handle so caller can stop the server
        with _SERVICE_LOCK: _SERVICE_CONTROL["httpd"] = httpd
        if sslc_local:
            cert_dir = os.path.join(MODEL_DIR, "certificates")
            cert, key = DGS(cert_dir)
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            context.load_cert_chain(certfile=cert, keyfile=key)
            httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
            print("[dearning] Cloud HTTPS is active at https://{}:{}".format(host_local,port))
        else: print("[dearning] Cloud HTTP is active at http://{}:{}".format(host_local,port))
        try: httpd.serve_forever()
        except KeyboardInterrupt: print("[dearning] Server stopped.")
        with _SERVICE_LOCK: _SERVICE_CONTROL["server_info"] = {"mode": mode, "host": host_local, "port": port, "sslc": sslc_local,}
    if threaded:
        t = threading.Thread(target=_start, daemon=daemon)
        with _SERVICE_LOCK: _SERVICE_CONTROL["thread"] = t
        t.start()
        print("[dearning] Server runs in the background (thread mode)")
        return t
    else: _start()

def stop_server(timeout: float = 5.0):
    global _DOMM_RUNNING
    _DOMM_RUNNING = False
    with _SERVICE_LOCK:
        httpd = _SERVICE_CONTROL.get("httpd")
        t = _SERVICE_CONTROL.get("thread")
    if not httpd: return False
    try:
        httpd.shutdown()
        httpd.server_close()
    except Exception: pass
    try:
        if t and t.is_alive(): t.join(timeout)
    except Exception: pass
    with _SERVICE_LOCK: _SERVICE_CONTROL.clear()
    return True

def _make_conn(host, port, sslc=True, timeout=30):
    if sslc:
        context = ssl._create_unverified_context()
        return http.client.HTTPSConnection(host, port, context=context, timeout=timeout)
    else: return http.client.HTTPConnection(host, port, timeout=timeout)

def post(host=DEFAULT_HOST, port=DEFAULT_PORT, model_path=None, password=DEFAULT_PASSWORD, sslc=False, timeout=60):
    '''This functiom is used to upload files to a server or network.

       example:
       >>> p = post(host="127.0.0.1", port=8080, model_path="C:\\Users\\...\\Documents\\your_file.py", password=4321, sslc=False, timeout=60)
       >>> print(p)'''
    if not model_path: raise ValueError("model_path cannot be empty")
    if isinstance(model_path, (str, bytes)): model_paths = [model_path]
    elif isinstance(model_path, (list, tuple)): model_paths = list(model_path)
    else: raise TypeError("model_path must be a string, list, or tuple")
    payload_files = []
    for path in model_paths:
        if not os.path.exists(path): raise FileNotFoundError(path)
        model_name = os.path.basename(path)
        with open(path, "rb") as fh: data = fh.read()
        b64 = base64.b64encode(data).decode("ascii")
        payload_files.append({"filename": model_name, "content_b64": b64})
    payload = {"password": password, "files": payload_files}
    body = json.dumps(payload).encode("utf-8")
    conn = _make_conn(host, port, sslc, timeout)
    try:
        try:
            sock = getattr(conn, "sock", None)
            if sock is not None: sock.settimeout(timeout)
        except Exception: pass
        conn.request("POST",  "/import_model", body=body, headers={"Content-Type": "application/json", "Content-Length": str(len(body))})
        r = conn.getresponse()
        raw = r.read()
        text = raw.decode("utf-8") if raw else ""
        try: j = json.loads(text) if text else None
        except Exception: j = {"status": r.status, "raw": text}
        if r.status != 200: return j or {"error": "server returned {}".format(r.status)}
        return j
    except (socket.timeout, TimeoutError): return {"error": "The server did not respond within the specified time."}
    except (ConnectionResetError, http.client.HTTPException, OSError) as e: return {"error": "connection error", "detail": str(e)}
    finally:
        try: conn.close()
        except Exception: pass

def load(host=DEFAULT_HOST, port=DEFAULT_PORT, filename=None, password=DEFAULT_PASSWORD, sslc=False, timeout=60, mode="code", save_path=None):
    '''This function is used to receive files and load files that have been sent by the post module.

        example:
        >>> l = load(host="127.0.0.1", port=8080, filename="your_file.py", password=4321, sslc=False, timeout=60, mode="code",)
        >>> print(l)'''
    if isinstance(filename, (str, bytes)): filenames = [filename]
    elif isinstance(filename, (list, tuple)): filenames = list(filename)
    else: raise TypeError("filename must be a string, list, or tuple")
    payload = {"password": password, "filenames": filenames}
    body = json.dumps(payload).encode("utf-8")
    conn = _make_conn(host, port, sslc, timeout)
    try:
        conn.request("POST", "/load_model", body=body, headers={"Content-Type": "application/json", "Content-Length": str(len(body))})
        r = conn.getresponse()
        raw = r.read()
        text = raw.decode("utf-8", errors="replace") if raw else ""
        j = json.loads(text) if text else {}
        if r.status != 200 or j.get("error"): return j
        files = j.get("files") or ([{"filename": j.get("filename"), "content_b64": j.get("content_b64")}] if j.get("content_b64") else [])
        results = {}
        for item in files:
            if not item or not item.get("content_b64"): continue
            fname = item.get("filename") or "<unknown>"
            try: # decode base64 -> raw file bytes
                data_b64 = item.get("content_b64") or ""
                data = base64.b64decode(data_b64)
            except Exception: continue
            if mode == "file":
                save_file = os.path.join(save_path or MODEL_DIR, fname)
                with open(save_file, "wb") as f: f.write(data)
                results[fname] = str(save_file)
            else:
                try:
                    decoded = data.decode("utf-8", errors="replace")
                    decoded = decoded.replace("\r\n", "\n").strip()
                    decoded = decoded.strip()
                    results[fname] = decoded
                except Exception: results[fname] = data
        if not results: raise FileNotFoundError("no files found or load failed")
        lines = ["=== {} ===\n{}".format(fname, content.decode("utf-8", errors="replace") if isinstance(content, (bytes, bytearray)) else content) for fname, content in results.items()]
        return "\n".join(lines).strip()
    finally:
        try: conn.close()
        except Exception: pass
