import dawdreamer
from logger import logger

try:
    engine = dawdreamer.RenderEngine(44100, 512)
    engine.set_bpm(120)
except Exception as e:
    logger.error(f"Error initializing DAW Dreamer: {e}")

def load_vst(vst_path):
    try:
        plugin = engine.make_plugin_processor("vst", vst_path)
        engine.load_graph({"nodes": [{"id": "vst", "processor": plugin}]})
    except Exception as e:
        logger.error(f"Failed to load VST {vst_path}: {e}")
