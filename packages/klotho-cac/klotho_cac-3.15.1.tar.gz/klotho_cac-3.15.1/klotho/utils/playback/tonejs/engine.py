import json
import uuid
from IPython.display import HTML, display

_TONEJS_CDN = "https://unpkg.com/tone@14.7.77/build/Tone.js"


def _convert_numpy_types(obj):
    try:
        import numpy as np
        if isinstance(obj, dict):
            return {k: _convert_numpy_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [_convert_numpy_types(v) for v in obj]
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        else:
            return obj
    except ImportError:
        return obj


class ToneEngine:
    def __init__(self, events):
        self.events = _convert_numpy_types(events)
        self.widget_id = f"klotho_{uuid.uuid4().hex[:8]}"
    
    def _generate_html(self):
        events_json = json.dumps(self.events)
        
        html = f'''
<div id="{self.widget_id}" style="
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 10px;
    background: #1a1a2e;
    border-radius: 6px;
    user-select: none;
">
    <button id="{self.widget_id}_btn" onclick="klotho_{self.widget_id}_toggle()" style="
        width: 32px;
        height: 32px;
        border: none;
        border-radius: 4px;
        background: #16213e;
        color: #e94560;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        transition: background 0.15s;
    ">&#9654;</button>
    <span id="{self.widget_id}_status" style="
        font-size: 11px;
        color: #a0a0a0;
        min-width: 50px;
    ">ready</span>
</div>

<script src="{_TONEJS_CDN}"></script>
<script>
var klotho_{self.widget_id}_isPlaying = false;
var klotho_{self.widget_id}_scheduledIds = [];
var klotho_{self.widget_id}_instruments = null;
var klotho_{self.widget_id}_events = {events_json};

function klotho_{self.widget_id}_toggle() {{
    var btn = document.getElementById("{self.widget_id}_btn");
    var statusEl = document.getElementById("{self.widget_id}_status");
    
    if (klotho_{self.widget_id}_isPlaying) {{
        klotho_{self.widget_id}_stop();
        klotho_{self.widget_id}_isPlaying = false;
        btn.innerHTML = "&#9654;";
        statusEl.textContent = "ready";
        statusEl.style.color = "#a0a0a0";
    }} else {{
        klotho_{self.widget_id}_isPlaying = true;
        btn.innerHTML = "&#9632;";
        statusEl.textContent = "playing";
        statusEl.style.color = "#e94560";
        klotho_{self.widget_id}_play();
    }}
}}

function klotho_{self.widget_id}_stop() {{
    try {{ Tone.Transport.stop(); }} catch(e) {{}}
    try {{ Tone.Transport.position = 0; }} catch(e) {{}}
    for (var i = 0; i < klotho_{self.widget_id}_scheduledIds.length; i++) {{
        try {{ Tone.Transport.clear(klotho_{self.widget_id}_scheduledIds[i]); }} catch(e) {{}}
    }}
    klotho_{self.widget_id}_scheduledIds = [];
    try {{ Tone.Transport.cancel(0); }} catch(e) {{}}
    
    if (klotho_{self.widget_id}_instruments) {{
        var insts = klotho_{self.widget_id}_instruments.instances;
        for (var k in insts) {{
            if (insts[k] && insts[k].releaseAll) {{ try {{ insts[k].releaseAll(); }} catch(e) {{}} }}
            if (insts[k] && insts[k].dispose) {{ try {{ insts[k].dispose(); }} catch(e) {{}} }}
        }}
        if (klotho_{self.widget_id}_instruments.master) {{
            try {{ klotho_{self.widget_id}_instruments.master.dispose(); }} catch(e) {{}}
        }}
        klotho_{self.widget_id}_instruments = null;
    }}
}}

function klotho_{self.widget_id}_play() {{
    Tone.start().then(function() {{
        klotho_{self.widget_id}_stop();
        
        var master = new Tone.Gain(0.9).toDestination();
        var instances = {{}};
        
        instances.synth = new Tone.PolySynth(Tone.Synth, {{
            maxPolyphony: 16,
            options: {{
                oscillator: {{ type: "triangle" }},
                envelope: {{ attack: 0.01, decay: 0.1, sustain: 0.3, release: 0.3 }}
            }}
        }});
        instances.synth.connect(master);
        
        instances.sine = new Tone.PolySynth(Tone.Synth, {{
            maxPolyphony: 32,
            options: {{
                oscillator: {{ type: "sine" }},
                envelope: {{ attack: 0.05, decay: 0.2, sustain: 0.5, release: 0.8 }}
            }}
        }});
        instances.sine.connect(master);
        
        instances.membrane = new Tone.MembraneSynth({{
            pitchDecay: 0.008,
            octaves: 6,
            envelope: {{ attack: 0.001, decay: 0.1, sustain: 0.0, release: 0.02 }}
        }});
        instances.membrane.connect(master);
        
        klotho_{self.widget_id}_instruments = {{ master: master, instances: instances }};
        
        var events = klotho_{self.widget_id}_events;
        var maxEnd = 0;
        
        for (var i = 0; i < events.length; i++) {{
            var ev = events[i];
            var end = ev.start + ev.duration;
            if (end > maxEnd) maxEnd = end;
            
            (function(evt) {{
                var id = Tone.Transport.schedule(function(time) {{
                    var inst = klotho_{self.widget_id}_instruments.instances[evt.instrument];
                    if (inst) {{
                        var pfields = evt.pfields || {{}};
                        var freq = pfields.freq || 440;
                        var vel = Math.max(0, Math.min(1, pfields.vel || 0.6));
                        inst.triggerAttackRelease(freq, evt.duration, time, vel);
                    }}
                }}, evt.start);
                klotho_{self.widget_id}_scheduledIds.push(id);
            }})(ev);
        }}
        
        var stopId = Tone.Transport.schedule(function() {{
            klotho_{self.widget_id}_stop();
            klotho_{self.widget_id}_isPlaying = false;
            var btn = document.getElementById("{self.widget_id}_btn");
            var statusEl = document.getElementById("{self.widget_id}_status");
            btn.innerHTML = "&#9654;";
            statusEl.textContent = "finished";
            statusEl.style.color = "#a0a0a0";
        }}, maxEnd + 0.3);
        klotho_{self.widget_id}_scheduledIds.push(stopId);
        
        Tone.Transport.start("+0.05");
    }});
}}
</script>
'''
        return html
    
    def display(self):
        html = self._generate_html()
        return display(HTML(html))
    
    def _repr_html_(self):
        return self._generate_html()
