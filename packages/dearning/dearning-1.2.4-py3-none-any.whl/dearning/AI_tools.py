import struct,logging,platform,math,os,random
from pathlib import Path
from dearning import cached

logger = logging.getLogger(__name__)

class DLP:
    '''DLP is a function for creating AI models that can analyze text.

    With the following functions:'''
    def __init__(self, lang="en"):
        self.lang = lang
        self.positive_words = {
        "Absolutely","Amazing","Best","Better","Breakthrough","Colossal","Destiny","Enormous","Excellent","Extraordinary","Famous","Fortune","Huge","Greatest","Growth","Mammoth",
        "Monumental","Outstanding","Powerful","Promising","Win","Remarkable","Results","Soar","Strong","Successful","Superior","Supreme","Triumph","Ultimate","Wonderful","Hot",
        "Attractive","Colorful","Daring","Delighted","Exciting","Magic","Fascinating","Important","Interesting","Pulse-pounding","Shocking","Startling","Strange","Surprising",
        "Thrilling","Zinger","Advantage","Advantageous","Beneficial","Brilliant","Convenient","Effective","Efficient","Enhance","Essential","Exceptional","Premium","Rare","Scarce",
        "Selected","Special","Unique","Immediately","Instant","Now","Urgent","Bargain","Bonus","Extra","Discount","Free","Freebie","Introductory","Liberal","Lowest","Reduced",
        "Refundable","Reward","Sale","Sampler","Savings","Valuable","Create","Discover","Edge","Innovative","Introducing","Invention","Launching","New","Pioneering","Revolutionary",
        "Approved","Authentic","Certified","Endorsed","Genuine","Guaranteed","Professional","Proven","Reliable","Tested","Trusted","Advice","Challenge","Empower","Energy","Focus",
        "Help","Improve","Increase","Inspire","Motivate","Opportunities","Perspective","Promote","Protect","Uplift","Compare","Complete","Expert","Fundamentals","Informative",
        "Instructive","Know","Learn","Practical","Revealin","Skill","Spotlight","Useful","Easy","Easily","Simple","Simplified","Simplistic","Beautiful","Lavishly","Luxury","Quality",
        "Safety","Secure","Security","Anniversary","Lifetime","Timely","Today","Trend","Trendy","Victory","Winning","Money","Profit","Profitable","Wealth","Affluent","Comfortable",
        "Flourish","Fortunate","Generous","Rich","Golden","Opulent","Thriving",}
        
        self.negative_words = {
        "bad","sad","hate","terrible","awful","poor","angry","Alert","Breaking","Alarming","Crisis","Danger","Risk","Threat","Warning","Deadline","Expire","Last","Limited","Miss",
        "Out","Disgusting","Infuriating","Outrageous","Revolting","Shameful","Heartbreaking","Hopeless","Lonely","Mournful","Tragic","Contaminated","Polluted","Toxic","Concealed",
        "Confidential","Odd","Unconventional","Unusual","Weird","Boring","Dull","Tedious","Uninspiring","Uninteresting","Unexciting","Common","Frequent","Ordinary","Routine","Usual",
        "Waste","Worthless","Damaged","Flawed","Shoddy","Broken","Cracked","Fractured","Injured","Sick","Unhealthy","Weak","Wounded","Accuse","Blame","Complain","Criticize","Denounce",
        "Disapprove","Scold","Insult","Offend","Ridicule","Mock","Disrespect","Disregard","Ignore","Neglect","Overlook","Reject","Abandon","Fail","Fumble","Misfire","Botch","Collapse",
        "Crash","Deteriorate","Decline","Worsen","Confuse","Mislead","Misunderstand","Mistake","Blunder","Stumble","Trip","Awkward","Clumsy","Inept","Incompetent","Unskilled",
        "Untrained","Unqualified","Unfit","Inadequate","Insufficient","Lacking","Deficient","Scam","Swindle","Cheat","Deceive","Fraud","Corrupt","Dishonest","Unethical","Immoral",
        "Illegal","Criminal","Unlawful","Misdemeanor",}

    @cached()
    def analyze_sentiment(self, text):
        words, word = [], ""
        for ch in text.lower():
            if ch.isalpha(): word += ch
            elif word:
                words.append(word)
                word = ""
        if word: words.append(word)
        total = len(words) or 1  
        pos_score = sum(1 for w in words if w in self.positive_words)
        neg_score = sum(1 for w in words if w in self.negative_words)
        polarity = (pos_score - neg_score) / total
        subjectivity = (pos_score + neg_score) / total
        if polarity > 0: label = "positive"
        elif polarity < 0: label = "negative"
        else: label = "neutral"
        return {"polarity": polarity,
                "subjectivity": subjectivity,
                "label": label}

    def extract_nouns(self, text):
        words = text.split()
        return [w.strip(".,!?") for w in words if w.istitle() and len(w) > 3]
    
    @cached()
    def pos_tagging(self, text): # aturan sederhana: kata kapital, ada 'ing' = VBG, default NN
        words = text.split()
        tags = []
        for w in words:
            if w.istitle(): tags.append((w, "NNP"))
            elif w.endswith("ing"): tags.append((w, "VBG"))
            else: tags.append((w, "NN"))
        return tags

    def summarize(self, text, max_sentences=2):
        sentences, temp = [], ""
        for ch in text:
            temp += ch
            if ch in ".!?":
                sentences.append(temp.strip())
                temp = ""
        if temp: sentences.append(temp.strip())
        summary = ". ".join(sentences[:max_sentences])
        if len(sentences) > max_sentences: summary += "."
        return summary
    
    @cached()
    def process(self, text):
        return {"sentiment": self.analyze_sentiment(text),
                "nouns": self.extract_nouns(text),
                "pos_tags": self.pos_tagging(text),
                "summary": self.summarize(text)}

class RLTools:
    class Env:
        def reset(self): raise NotImplementedError
        def step(self, action): raise NotImplementedError
        def actions(self): raise NotImplementedError
        def state(self): raise NotImplementedError
    class SimpleEnv(Env):
        def __init__(self, start=0, goal=10, min_s=-10, max_s=10):
            self.start = start
            self.goal = goal
            self.min_s = min_s
            self.max_s = max_s
            self.s = start
        def reset(self): return self.start
        def state(self): return self.s
        def actions(self): return (-1, 1)
        def step(self, action):
            self.s += action
            self.s = max(self.min_s, min(self.max_s, self.s))
            r = 1.0 if self.s == self.goal else -0.01
            done = self.s == self.goal
            return self.s, r, done
    class Policy:
        def select(self, q, s, acts): raise NotImplementedError
    class EpsilonGreedy(Policy):
        def __init__(self, eps=0.1): self.eps = eps
        def select(self, q, s, acts):
            if random.random() < self.eps: return random.choice(acts)
            best = best_v = None
            for a in acts:
                v = q.get((s,a), 0.0)
                if best_v is None or v > best_v:
                    best_v = v
                    best = a
            return best
    class Softmax(Policy):
        def __init__(self, temp=1.0): self.temp = temp
        def select(self, q, s, acts):
            vals = [math.exp(q.get((s,a),0.0)/self.temp) for a in acts]
            r = random.random()
            c = 0.0
            for a,v in zip(acts,vals):
                c += v/sum(vals)
                if r <= c: return a
            return acts[-1]
    class Replay:
        def __init__(self, maxlen=1000):
            import collections
            self.buf = collections.deque(maxlen=maxlen)
        def push(self, item): self.buf.append(item)
        def sample(self, n):
            if n >= len(self.buf): return list(self.buf)
            return random.sample(self.buf, n)
        def __len__(self): return len(self.buf)
    class Agent:
        def __init__(self, policy=None, alpha=0.1, gamma=0.9):
            self.q = {}
            self.alpha = alpha
            self.gamma = gamma
            self.policy = policy or RLTools.EpsilonGreedy()
        def act(self, s, acts): return self.policy.select(self.q, s, acts)
        def update(self, s, a, r, ns, na=None, terminal=False):
            old = self.q.get((s,a),0.0)
            if terminal: target = r
            else:
                if na is None:
                    m = None
                    for aa in (): pass
                    m = max(self.q.get((ns,aa),0.0) for aa in self._acts)
                    target = r + self.gamma*m
                else: target = r + self.gamma*self.q.get((ns,na),0.0)
            self.q[(s,a)] = old + self.alpha*(target-old)
        def bind_actions(self, acts): self._acts = acts
    class Logger:
        def __init__(self): self.data = []
        def log(self, **kw):
            import time
            self.data.append((time.time(), kw))
        def summary(self): return self.data
    class Trainer:
        def __init__(self, env, agent, episodes=1000, max_steps=100, mode="q"):
            self.env = env
            self.agent = agent
            self.episodes = episodes
            self.max_steps = max_steps
            self.mode = mode
            self.logger = RLTools.Logger()
            self.replay = None
        def use_replay(self, size=1000): self.replay = RLTools.Replay(size)
        def train(self):
            acts = self.env.actions()
            self.agent.bind_actions(acts)
            for ep in range(self.episodes):
                s = self.env.reset()
                total = 0.0
                a = self.agent.act(s, acts)
                for t in range(self.max_steps):
                    ns, r, done = self.env.step(a)
                    total += r
                    if self.mode == "sarsa":
                        na = self.agent.act(ns, acts)
                        self.agent.update(s,a,r,ns,na,done)
                        s,a = ns,na
                    else:
                        self.agent.update(s,a,r,ns,None,done)
                        s = ns
                        a = self.agent.act(s,acts)
                    if self.replay:  self.replay.push((s,a,r,ns))
                    if done: break
                self.logger.log(ep=ep,reward=total)
            return self.logger
    class Evaluator:
        def __init__(self, env, agent):
            self.env = env
            self.agent = agent
        def run(self, episodes=100):
            acts = self.env.actions()
            self.agent.bind_actions(acts)
            scores = []
            for _ in range(episodes):
                s = self.env.reset()
                total = 0.0
                for _ in range(100):
                    a = self.agent.act(s,acts)
                    s,r,d = self.env.step(a)
                    total += r
                    if d: break
                scores.append(total)
            return {"mean": sum(scores)/len(scores) if scores else 0.0,
                    "max": max(scores) if scores else 0.0, "min": min(scores) if scores else 0.0}
    class Hook:
        def __init__(self): self.h = {}
        def add(self, name, fn): self.h.setdefault(name,[]).append(fn)
        def call(self, name, *a, **k):
            for fn in self.h.get(name,[]): fn(*a,**k)
    class Engine:
        def __init__(self): self.hook = RLTools.Hook()
        def on(self, name, fn): self.hook.add(name,fn)
        def emit(self, name, *a, **k): self.hook.call(name,*a,**k)
    class Runner:
        def __init__(self, trainer):
            self.trainer = trainer
            self.engine = RLTools.Engine()
        def run(self):
            self.engine.emit("start")
            log = self.trainer.train()
            self.engine.emit("end", log)
            return log
    @staticmethod
    def build_simple_q(episodes=500): return RLTools.Trainer(RLTools.SimpleEnv(), RLTools.Agent(), episodes=episodes)

class image:
    @staticmethod
    def load(path, target_size=None, grayscale=False):
        if not path or not os.path.exists(path): raise ValueError("File not found.")
        ext = os.path.splitext(path)[1].lower()
        def _load_pnm(p):
            with open(p, "rb") as f:
                header = f.readline().strip()
                if header not in (b"P5", b"P6"): raise ValueError("PNM invalid (must be P5/P6).")
                dims = f.readline().strip()
                while dims.startswith(b"#"): dims = f.readline().strip()
                w, h = map(int, dims.split())
                maxval = int(f.readline().strip())
                raw = f.read()
            pix = [v / maxval for v in raw]
            ch  = 1 if header == b"P5" else 3
            return pix, (w, h), ch
        def _load_png(path): # returns (pix_list_float, (w,h), channels)
            with open(path, "rb") as f: data = f.read()
            if len(data) < 8 or data[:8] != b'\x89PNG\r\n\x1a\n': raise ValueError("Not a valid PNG file")
            chunks = _read_chunks(data)
            ihdr = None
            palette = None
            trns = None
            idat_concat = b""
            color_type = None
            bitdepth = None
            width = height = None
            compression = None
            filter_method = None
            interlace = 0
            for ctype, cdata in chunks:
                if ctype == b'IHDR':
                    width, height, bitdepth, color_type, compression, filter_method, interlace = struct.unpack(">IIBBBBB", cdata)
                    ihdr = (width, height, bitdepth, color_type, compression, filter_method, interlace)
                elif ctype == b'PLTE': palette = [(int(cdata[i]), int(cdata[i+1]), int(cdata[i+2])) for i in range(0, len(cdata), 3)]
                elif ctype == b'tRNS': trns = cdata
                elif ctype == b'IDAT': idat_concat += cdata
                elif ctype == b'IEND': break
            if ihdr is None: raise ValueError("Missing IHDR")
            width, height, bitdepth, color_type, compression, filter_method, interlace = ihdr
            # validate
            if compression != 0 or filter_method != 0: raise ValueError("Unsupported PNG compression/filter method")
            if color_type not in (0,1,2,3,4,6): raise ValueError("Unsupported color type: %r" % (color_type,)) # 1 is not valid; standard uses 0,2,3,4,6. Keep defensive.
            # channels mapping: 0: grayscale, 2: truecolor RGB, 3: palette, 4: grayscale + alpha, 6: truecolor + alpha (RGBA)
            if color_type == 0: channels = 1
            elif color_type == 2: channels = 3
            elif color_type == 3: channels = 1  # indices (will expand with palette)
            elif color_type == 4: channels = 2
            elif color_type == 6: channels = 4
            else: channels = 1
            raw_img = _inflate_idat_chunks(idat_concat) # decompress IDAT
            # handle interlace
            if interlace == 0: samples = _decode_noninterlaced(raw_img, width, height, bitdepth, channels)
            else: samples = _deinterlace_adam7(raw_img, width, height, bitdepth, channels)
            # handle palette expand
            if color_type == 3: # samples are palette indices (0..)
                if palette is None: raise ValueError("Palette image without PLTE")
                pal_rgba = _apply_trns_to_palette(palette, trns)
                # expand per-pixel RGBA or RGB depending on padding
                # For palette images, if tRNS present then we have alpha; else alpha=255
                has_alpha = trns is not None
                out = [c for idx in samples for c in (pal_rgba[idx] if has_alpha else pal_rgba[idx][:3])]
                # after expansion, set channels accordingly
                if has_alpha: channels = 4
                else: channels = 3
                # samples now bytes 0..255 per channel; map bitdepth scale if bitdepth != 8? palette format uses 8-bit entries
                samples = out
                bitdepth = 8
            else:
                # handle tRNS for grayscale or truecolor
                if trns is not None:
                    if color_type == 0:
                        # grayscale: single sample value -> alpha where equal to value
                        alpha_map_val = None
                        if len(trns) >= 2: alpha_map_val = (ord(trns[0:1])<<8) | ord(trns[1:2]) if bitdepth==16 else ord(trns[0:1])
                        out = [x for s in samples for x in (s, 255 if bitdepth == 16 else (0 if alpha_map_val is not None and s == alpha_map_val else 255))] # pair of bytes: already handled earlier; but tRNS for 16-bit grayscale would be 2 bytes
                        samples = out
                        channels = 2
                        bitdepth = 8 if bitdepth < 8 else bitdepth
                    elif color_type == 2: # tRNS contains r,g,b of color to be considered transparent and compare triplets
                        tr = None
                        if bitdepth == 16 and len(trns) >= 6: tr = ((ord(trns[0:1])<<8)|ord(trns[1:2]), (ord(trns[2:3])<<8)|ord(trns[3:4]), (ord(trns[4:5])<<8)|ord(trns[5:6]))
                        elif len(trns) >= 3: tr = (ord(trns[0:1]), ord(trns[1:2]), ord(trns[2:3]))
                        if tr is not None:
                            out = [c for r, g, b in zip(samples[0::3], samples[1::3], samples[2::3]) for c in ((r, g, b, 0) if (r, g, b) == tr else (r, g, b, 255))]
                            samples = out
                            channels = 4
                            bitdepth = 8
                # At this point, samples is a list of integer sample values per channel (may be 0..(2^bitdepth-1) or 0..255)
                # Convert 16-bit samples to integer values if needed (already done), then convert to floats 0..1
                # Handle 16-bit mapping
                if bitdepth == 16: floats = [float(s) / 65535.0 for s in samples] # ensure samples are 0..65535
                else: floats = [float(s) / float((1<<bitdepth)-1) if bitdepth>0 else float(s) for s in samples]
            def _bytes_to_int(b): return int(b.encode('hex') if False else 0)
            def _unpack(fmt, data): return struct.unpack(fmt, data)
            def _paeth(a, b, c):
                p = a + b - c
                pa = abs(p - a)
                pb = abs(p - b)
                pc = abs(p - c)
                return a if pa<=pb and pa<=pc else (b if pb<=pc else c)
            def _read_chunks(data):
                i = 8  
                chunks = []
                while i + 8 <= len(data):
                    length = struct.unpack(">I", data[i:i+4])[0]; i += 4
                    ctype = data[i:i+4]; i += 4
                    chunk = data[i:i+length]; i += length
                    crc = data[i:i+4]; i += 4
                    chunks.append((ctype, chunk))
                return chunks
            def _expand_bits_to_bytes(bitarr, bitdepth, width, channels): # bitarr is sequence of bytes representing packed samples (for bitdepth < 8)
                samples_per_byte = 8 // bitdepth
                mask = (1 << bitdepth) - 1
                out = [((v >> shift) & mask) for b in bitarr for v in [(ord(b) if isinstance(b, bytes) and len(b)==1 else b)] for shift in reversed(range(0, 8, bitdepth))]
                total = width * channels
                return out[:total]
            def _unpack_samples_from_scanline(scan_bytes, bitdepth, channels, width): # returns list of samples (integers) for the scanline: len = width * channels
                if bitdepth == 8: return list(scan_bytes[:width*channels]) # straightforward
                samples = [((a<<8)|b) for a,b in (((ord(scan_bytes[i]) if isinstance(scan_bytes[i], bytes) and len(scan_bytes[i])==1 else scan_bytes[i]), (ord(scan_bytes[i+1]) if isinstance(scan_bytes[i+1], bytes) and len(scan_bytes[i+1])==1 else scan_bytes[i+1])) for i in range(0, width*channels*2, 2))]
                bits = [ord(b) if isinstance(b, bytes) and len(b) == 1 else b for b in scan_bytes] # bitdepth 1/2/4
                samples = _expand_bits_to_bytes(bits, bitdepth, width, channels) # expand
                return samples[:width*channels]
            def _filter_restore(prev, scan, filter_type, bpp):
                # prev: list ints previous scanline samples (raw bytes or samples depending)
                # scan: list ints current scanline (raw bytes)
                # bpp: bytes per pixel in bytes (for filter algorithm indexing), for sample-level we adapt
                if filter_type == 0: return scan
                if filter_type == 1: # Sub
                    return [((scan[i] + (out[i-bpp] if i >= bpp else 0)) & 0xFF) for i in range(len(scan)) for out in [locals().setdefault("_ho_sub", [])] if not out.append((scan[i] + (out[i-bpp] if i>=bpp else 0)) & 0xFF)] 
                if filter_type == 2: # Up
                    [((scan[i] + (prev[i] if prev is not None and i < len(prev) else 0)) & 0xFF) for i in range(len(scan))] 
                if filter_type == 3: # Average
                    return [((scan[i] + (((out[i-bpp] if i>=bpp else 0) + (prev[i] if prev is not None and i < len(prev) else 0)) // 2)) & 0xFF) for i in range(len(scan))  for out in [locals().setdefault("_o_avg", [])] if not out.append((scan[i] + (((out[i-bpp] if i>=bpp else 0) + (prev[i] 
                     if prev is not None and i < len(prev) else 0)) // 2)) & 0xFF)]
                if filter_type == 4: # Paeth
                    return [((scan[i] + _paeth((out[i-bpp] if i>=bpp else 0), (prev[i] if prev is not None and i < len(prev) else 0), (prev[i-bpp] if (prev is not None and i>=bpp and i < len(prev)) else 0))) & 0xFF) 
                     for i in range(len(scan)) for out in [locals().setdefault("_o_pth", [])] if not out.append((scan[i] + _paeth((out[i-bpp] if i>=bpp else 0), (prev[i] if prev is not None and i < len(prev) else 0), (prev[i-bpp] if (prev is not None and i>=bpp and i < len(prev)) else 0))) & 0xFF)] 
                raise ValueError("Unknown filter: %r" % (filter_type,))
            def _samples_to_float(samples, bitdepth): # convert integer sample list to float 0.0..1.0
                if bitdepth == 16: denom = float((1 << 16) - 1)
                else: denom = float((1 << bitdepth) - 1)
                return [s / denom for s in samples]
            def _deinterlace_adam7(raw_idat, width, height, bitdepth, channels):
                # raw_idat: decompressed concatenation of interlaced IDAT data (bytes)
                # produce final image samples list as bytes (per-sample integers), length = width*height*channels
                # For Adam7, each pass has its own scanlines with filter bytes.
                _ADAM7 = [(0, 0, 8, 8),(4, 0, 8, 8),(0, 4, 4, 8),(2, 0, 4, 4),(0, 2, 2, 4),(1, 0, 2, 2),(0, 1, 1, 2),]
                final = [0] * (width * height * channels)  # sample ints
                for pass_idx, (start_col, start_row, col_step, row_step) in enumerate(_ADAM7): # compute size of this pass
                    pw = (width - start_col + col_step - 1) // col_step
                    ph = (height - start_row + row_step - 1) // row_step
                    if pw <= 0 or ph <= 0: continue
                    if bitdepth >= 8:
                        bpp_bytes = (channels * (bitdepth // 8))
                        scanline_len = pw * channels * (bitdepth // 8)
                    else: # packed bits; width in samples converted to bytes ceil()
                        bits_per_scan = pw * channels * bitdepth
                        scanline_len = (bits_per_scan + 7) // 8
                        bpp_bytes = max(1, (channels * ((bitdepth+7)//8)))
                    prev = None
                    ptr = 0
                    for row in range(ph):
                        if ptr >= len(raw_idat): raise ValueError("IDAT truncated while reading Adam7")
                        filter_type = ord(raw_idat[ptr:ptr+1]) if isinstance(raw_idat[ptr:ptr+1], bytes) else raw_idat[ptr]
                        ptr += 1
                        scan = list(bytearray(raw_idat[ptr:ptr+scanline_len]))
                        ptr += scanline_len
                        restored = _filter_restore(prev, scan, filter_type, bpp_bytes)
                        prev = restored
                        samples = _unpack_samples_from_scanline(restored, bitdepth, channels, pw) # unpack samples from restored bytes
                        # place samples into final image at (start_row + row*row_step) and columns accordingly
                        out_row = start_row + row * row_step
                        col_idx = 0
                        for col in range(pw):
                            out_col = start_col + col * col_step
                            for ch in range(channels):
                                src_sample = samples[col_idx]
                                col_idx += 1
                                dst_index = ((out_row * width) + out_col) * channels + ch
                                final[dst_index] = src_sample
                return final
            def _decode_noninterlaced(raw_idat, width, height, bitdepth, channels): # raw_idat is decompressed bytes of concatenated scanlines with filter type bytes at start
                ptr = 0
                prev = None
                scanline_len = width*channels*(bitdepth//8) if bitdepth>=8 else ((width*channels*bitdepth+7)//8)
                stride = max(1, channels*(bitdepth//8) if bitdepth>=8 else 1)
                final = []
                for _ in range(height):
                    if ptr >= len(raw_idat): raise ValueError("IDAT truncated while decoding")
                    ft = raw_idat[ptr] if not isinstance(raw_idat[ptr:ptr+1], bytes) else ord(raw_idat[ptr:ptr+1]); ptr += 1
                    scan = bytearray(raw_idat[ptr:ptr+scanline_len]); ptr += scanline_len
                    prev = _filter_restore(prev, scan, ft, stride)
                    final += [v for v in _unpack_samples_from_scanline(prev, bitdepth, channels, width)]
                return final
            def _inflate_idat_chunks(idat_bytes_concat): # attempt with raw inflate
                import zlib
                try: return zlib.decompress(idat_bytes_concat)
                except Exception:
                    try: return zlib.decompressobj().decompress(idat_bytes_concat) + zlib.decompressobj().flush()
                    except Exception: raise
            def _apply_trns_to_palette(palette, trns): return [(r, g, b, (ord(trns[i:i+1]) if isinstance(trns[i:i+1], bytes) else trns[i]) if trns and i < len(trns) else 255) for i, (r, g, b) in enumerate(palette)] # palette: list of tuples (r,g,b) each 0..255, trns: bytes of alpha entries or None
            def _expand_palette_to_pixels(palette, pixels_idx, bitdepth): return [palette[i] for i in pixels_idx] # pixels_idx: list of palette indices (per sample)
            def _normalize_samples_to_float(samples, bitdepth, channels): return [s / float(((1<<bitdepth)-1) if bitdepth!=16 else 65535) for s in samples]
            def _pack_pixels_interleaved_rgb(samples, ch, bitdepth): return _normalize_samples_to_float(samples, bitdepth, ch) # samples is list of sample ints interleaved; convert to floats and return list of floats
            def load_image(path=None, target_size=None, grayscale=False): # Public wrapper for integration with earlier image class
                if path is None: # path may be None -> return dummy
                    w, h = (target_size if target_size else (64, 64))
                    ch = 1 if grayscale else 3
                    if ch == 1: return [((i+j) % 256)/255.0 for i in range(h) for j in range(w)], (w,h), ch
                    else: return [((i+j) % 256)/255.0 for i in range(h) for j in range(w) for _ in range(3)], (w,h), ch
                # detect ext
                path_l = path.lower()
                if path_l.endswith(".pgm") or path_l.endswith(".ppm"):
                    with open(path, "rb") as f: # simple PNM loader
                        header = f.readline().strip()
                        while header == b'': header = f.readline().strip()
                        if header not in (b'P5', b'P6'): raise ValueError("PNM only P5/P6 supported")
                        dims = b'' # read dims
                        while True:
                            line = f.readline()
                            if not line: break
                            if line.startswith(b'#'): continue
                            dims = line.strip()
                            break
                        parts = dims.split()
                        w = int(parts[0]); h = int(parts[1])
                        maxv = int(f.readline().strip())
                        raw = f.read()
                        if header == b'P5':
                            ch = 1
                            pix = [float(ord(c))/float(maxv) if isinstance(c, bytes) and len(c)==1 else float(c)/float(maxv) for c in raw[:w*h]]
                        else:
                            ch = 3
                            pix = [(raw[i+j] if not isinstance(raw[i+j], bytes) else ord(raw[i+j])) / float(maxv) for i in range(0, min(len(raw), w*h*3), 3) for j in (0, 1, 2)]
                        if grayscale and ch == 3:
                            pix = [(pix[i]+pix[i+1]+pix[i+2])/3.0 for i in range(0, len(pix), 3)]
                            ch = 1
                        if target_size: # simple nearest-neighbor resize (conservative)
                            tw, th = target_size
                            src_w, src_h = w, h
                            if ch == 1: newpix = [pix[int(yy*src_h/th)*src_w + int(xx*src_w/tw)] for yy in range(th) for xx in range(tw)]
                            else: newpix = [pix[i] for yy in range(th) for xx in range(tw) for i in ((sy*src_w+sx)*3 + k for k in (0,1,2)) for sy,sx in ((int(yy*src_h/th), int(xx*src_w/tw)),)]
                            pix = newpix
                            w, h = tw, th
                        return pix, (w, h), ch
                else: # png route
                    pix, size, ch = _load_png(path)
                    w, h = size
                    if grayscale and ch >= 3: # convert RGB/RGBA to grayscale
                        if ch == 4: rgb = [(pix[i]*0.2989 + pix[i+1]*0.5870 + pix[i+2]*0.1140) for i in range(0, len(pix), 4)]
                        else: rgb = [(pix[i]*0.2989 + pix[i+1]*0.5870 + pix[i+2]*0.1140) for i in range(0, len(pix), 3)]
                        pix = rgb
                        ch = 1
                    if target_size: # nearest neighbor resize
                        tw, th = target_size
                        if ch == 1: newpix = [pix[int(yy*h/float(th))*w + int(xx*w/float(tw))] for yy in range(th) for xx in range(tw)]
                        else: newpix = [pix[(int(yy*h/float(th))*w + int(xx*w/float(tw)))*ch + c] for yy in range(th) for xx in range(tw) for c in range(ch)]
                        pix = newpix
                        w, h = tw, th
                    return pix, (w, h), ch
            return floats, (width, height), channels
    @staticmethod
    def resize(pix, w, h, target, is_rgb):
        tw = th = target
        if is_rgb: return sum((pix[idx:idx+3] for ty in range(th) for tx in range(tw) for idx in [(int((ty*h)/th) * w * 3 + int((tx*w)/tw) * 3)]), [])
        else:
            ry = [(ty*h)//th * w for ty in range(th)]
            rx = [(tx*w)//tw for tx in range(tw)]
            return [pix[ry[y] + rx[x]] for y in range(th) for x in range(tw)]
    @staticmethod
    def flatten(pix): return list(pix)
    @staticmethod
    def save(path, pix, size, ch=1):
        w = h = size
        if ch == 1:
            header = b"P5\n%d %d\n255\n" % (w, h)
            data = bytearray(int(p * 255) for p in pix)
        else:
            header = b"P6\n%d %d\n255\n" % (w, h)
            data = bytearray(int(p * 255) for p in pix)
        with open(path, "wb") as f:
            f.write(header)
            f.write(data)

class video:
    def gif(path, target_size=None, as_rgba=True, max_frames=None):
        f = open(path, "rb")
        try:
            hdr = _parse_header(f)
            W = hdr["width"]; H = hdr["height"]
            gct_raw = hdr["gct"]
            gct = _read_color_table(gct_raw, hdr["gct_size"]) if gct_raw else None
            frames_out = []
            loop_count = 1
            curr_canvas = bytearray([0]* (W*H*4))
            # initialize bg
            if gct and hdr["bg_index"] < len(gct):
                r,g,b = gct[hdr["bg_index"]]
                mv = memoryview(curr_canvas)
                mv[0::4] = bytes([r]) * (len(mv)//4)
                mv[1::4] = bytes([g]) * (len(mv)//4)
                mv[2::4] = bytes([b]) * (len(mv)//4)
                mv[3::4] = b"\xff" * (len(mv)//4)
            gce = {"delay": 10, "transparent_index": None, "disposal": 0}
            frames = []
            while True:
                b = f.read(1)
                if not b: break
                ch = b[0] if isinstance(b, bytes) else b
                if ch == 0x3B: break
                if ch == 0x21: # extension
                    label_b = _read_bytes(f,1)
                    label = ord(label_b) if isinstance(label_b, bytes) else label_b
                    if label == 0xF9: # Graphic Control Extension
                        _ = _read_bytes(f,1) # block size (should be 4)
                        packed = ord(_read_bytes(f,1))
                        delay_bytes = _read_bytes(f,2)
                        delay = struct.unpack("<H", delay_bytes)[0]
                        transp = ord(_read_bytes(f,1))
                        _ = _read_bytes(f,1) # block terminator
                        disp = (packed & 0x1C) >> 2
                        transp_index = transp if (packed & 1) else None
                        gce = {"delay": max(delay,1), "transparent_index": transp_index, "disposal": disp}
                    elif label == 0xFF: # Application Extension
                        _, app = (_read_bytes(f,1), _read_bytes(f,8))
                        data = _read_subblocks(f)
                        if app == b"NETSCAPE" and len(data) >= 3 and data[0] == 1: loop_count = data[1] | (data[2] << 8)
                    else:  _ = _read_subblocks(f)
                elif ch == 0x2C: # image descriptor
                    idata = _read_bytes(f,9)
                    ix, iy, iw, ih, packed = struct.unpack("<HHHHB", idata)
                    lct_flag = (packed & 0x80) >> 7
                    interlace = (packed & 0x40) >> 6
                    lct_size = 2 ** ((packed & 0x07) + 1) if lct_flag else 0
                    lct = None
                    lct = _read_color_table(_read_bytes(f, 3*lct_size), lct_size) if lct_flag else None
                    palette = lct if lct is not None else gct
                    if palette is None: raise ValueError("No color table for image")
                    lzw_min = ord(_read_bytes(f,1))
                    idat = _read_subblocks(f)
                    raw_pixels = _lzw_decode(lzw_min, idat) # decode LZW
                    # raw_pixels is stream of palette indices or RGB depending on bpp; for GIF it's palette indices per pixel
                    bpp_channels = 1  # indices
                    pixels = (_deinterlace_adam7(list(raw_pixels), iw, ih, bpp_channels) if interlace else list(raw_pixels))
                    # apply local palette -> produce byte values
                    # Compose onto canvas copy depending on disposal
                    prev_canvas = bytearray(curr_canvas)  # before applying
                    # convert palette indices to bytes (0..255)
                    # For internal compose, we keep palette indices for ch==1 case
                    _compose_frame((curr_canvas, None, W, H), pixels, ix, iy, iw, ih, gce["disposal"], gce["transparent_index"], palette)
                    duration_ms = int(gce.get("delay", 10) * 10) # capture frame
                    # copy of canvas to output
                    outbuf = bytearray(curr_canvas)
                    if target_size is not None: # simple nearest-neighbor resize (optional)
                        tw, th = target_size
                        scaled = _resize_canvas(outbuf, W, H, tw, th)
                        outbuf = scaled; outW = tw; outH = th
                    else: outW, outH = W, H
                    pixel_float = _to_float_list(outbuf, outW, outH, 4) if as_rgba else _to_float_list(outbuf, outW, outH, 3) # convert to float list if requested
                    frames_out.append((pixel_float, (outW, outH), 4 if as_rgba else 3, duration_ms))
                    frames.append({"delay":duration_ms, "disposal":gce["disposal"], "transparent_index":gce["transparent_index"]})
                    if gce["disposal"] == 2: # handle disposal
                        if gct and hdr["bg_index"] < len(gct): # restore to background color
                            r,g,b = gct[hdr["bg_index"]]
                            for yy in range(iy, iy+ih):
                                if yy<0 or yy>=H: continue
                                base = (yy*W + ix)*4
                                for xx in range(iw):
                                    if ix+xx<0 or ix+xx>=W: continue
                                    off = base + xx*4
                                    curr_canvas[off] = r; curr_canvas[off+1]=g; curr_canvas[off+2]=b; curr_canvas[off+3]=255
                    elif gce["disposal"] == 3: curr_canvas = prev_canvas # restore to previous
                    else: pass # disposal 0 or 1: keep as is
                    gce = {"delay": 10, "transparent_index": None, "disposal": 0} # reset GCE
                    if max_frames and len(frames_out) >= max_frames: break
                else: pass
        
            def _read_bytes(f, n):
                b = f.read(n)
                if len(b) != n: raise EOFError("Unexpected EOF")
                return b

            def _read_subblocks(f):
                out = bytearray()
                while True:
                    b = f.read(1)
                    if not b: raise EOFError("Unexpected EOF")
                    n = ord(b)
                    if n == 0: break
                    out.extend(f.read(n))
                return bytes(out)

            def _parse_header(f):
                sig = _read_bytes(f, 6)
                if not (sig.startswith(b"GIF87a") or sig.startswith(b"GIF89a")): raise ValueError("Not a GIF")
                lsd = _read_bytes(f, 7)
                w, h, packed, bg, ratio = struct.unpack("<HHBBB", lsd)
                gct_flag = (packed & 0x80) >> 7
                color_res = ((packed & 0x70) >> 4) + 1
                gct_size = 2 ** ((packed & 0x07) + 1) if gct_flag else 0
                gct = None
                if gct_flag: gct = list(_read_bytes(f, 3 * gct_size))
                return {"width": w, "height": h, "gct": gct, "gct_size": gct_size, "bg_index": bg, "aspect": ratio, "color_res": color_res}

            def _read_color_table(raw, size):
                if raw is None: return None
                assert len(raw) >= 3 * size
                return [tuple((raw[j] if isinstance(raw[j], int) else ord(raw[j:j+1])) for j in (3*i,3*i+1,3*i+2)) for i in range(size)]


            def _deinterlace_adam7(pixels, w, h, bpp):
                out = [0]*(w*h*bpp)
                idx = 0
                _ADAM7 = [(0,0,8,8),(4,0,8,8),(0,4,4,8),(2,0,4,4),(0,2,2,4),(1,0,2,2),(0,1,1,2)]
                for sx, sy, dx, dy in _ADAM7:
                    for y in range(sy, h, dy):
                        row = y*w*bpp
                        for x in range(sx, w, dx):
                            out[row+x*bpp:row+x*bpp+bpp] = pixels[idx:idx+bpp]
                            idx += bpp
                return out

            def _lzw_decode(min_code_size, data): # LZW decoder for GIF
                bit_stream = [b if isinstance(b, int) else ord(b) for b in data] # data is bytes of subblocks concatenated
                # build bit pointer
                bits = cur = 0
                def get_bits(n):
                    nonlocal bits, cur
                    acc = 0
                    bitpos = 0
                    while bitpos < n:
                        if bits == 0:
                            if cur >= len(bit_stream): raise EOFError("LZW stream ended")
                            curbyte = bit_stream[cur]
                            cur += 1
                            bits = 8
                            acc_byte = curbyte
                        take = min(bits, n - bitpos)
                        shift = bits - take
                        part = (acc_byte >> shift) & ((1 << take) - 1)
                        acc = (acc << take) | part
                        bits -= take
                        acc_byte = acc_byte & ((1 << shift) - 1) if shift > 0 else 0
                        bitpos += take
                    return acc
                clear_code = 1 << min_code_size
                end_code = clear_code + 1
                code_size = min_code_size + 1
                dict_reset = {i: bytes([i]) for i in range(clear_code)}
                dict_reset[clear_code] = None
                dict_reset[end_code] = None
                next_code = end_code + 1
                out = bytearray()
                old = prev_entry = None
                try:
                    while True:
                        code = get_bits(code_size)
                        if code == clear_code:
                            code_size, next_code, old = min_code_size + 1, end_code + 1, None
                            continue
                        if code == end_code: break
                        entry = dict_reset.get(code, prev_entry + prev_entry[:1])
                        out.extend(entry)
                        if old:
                            dict_reset[next_code] = old + entry[:1]
                            next_code += 1
                            if next_code >= (1 << code_size) and code_size < 12: code_size += 1
                        prev_entry = old = entry
                except EOFError: pass
                return bytes(out)

            def _compose_frame(canvas, fp, x, y, fw, fh, ch, disp, tr, pal):
                buf, _, W, H = canvas
                idx = 0
                for yy in range(fh):
                    ry = y + yy
                    if not (0 <= ry < H):
                        idx += fw * ch
                        continue
                    base = (ry * W + x) * 4
                    for xx in range(fw):
                        rx = x + xx
                        if not (0 <= rx < H):
                            idx += ch
                            continue
                        if ch == 1:
                            p = fp[idx]; idx += 1
                            if p == tr: continue
                            r, g, b = pal[p]
                        else:
                            r, g, b = fp[idx:idx+3]
                            idx += ch
                        o = base + xx*4
                        buf[o:o+4] = (r, g, b, 255)
                return buf

            def _to_float_list(buf, w, h, channels=4):
                out = [0.0] * (w*h*channels)
                for i, v in enumerate(buf): out[i] = float(v) / 255.0
                return out

            def _resize_canvas(buf, W, H, TW, TH): # small nearest-neighbor resize for RGBA bytearray
                out = bytearray(TW*TH*4)
                for y in range(TH):
                    sy = int(y * H / TH)
                    if sy >= H: sy = H-1
                    for x in range(TW):
                        sx = int(x * W / TW)
                        if sx >= W: sx = W-1
                        sidx = (sy*W + sx)*4
                        didx = (y*TW + x)*4
                        out[didx:didx+4] = buf[sidx:sidx+4]
                return out
        finally:
            try: f.close()
            except: pass

class Qkanalyze:
    @cached()
    def top_kprobs(preds, k=3):
        '''Take the K largest probabilities from the list.'''
        sorted_idx = sorted(range(len(preds)), key=lambda i: preds[i], reverse=True)
        return [(i, float(preds[i])) for i in sorted_idx[:k]]

    @cached()
    def summarize_array(arr):
        '''Summary of 1D or 2D list values.''' # flatten kalau nested list
        flat = [x for row in arr for x in (row if isinstance(row, (list, tuple)) else [row])]
        return {"min": float(min(flat)), "max": float(max(flat)),
                "mean": float(sum(flat)/len(flat)),
                "shape": (len(arr), len(arr[0]) if isinstance(arr[0], (list, tuple)) else 1)}