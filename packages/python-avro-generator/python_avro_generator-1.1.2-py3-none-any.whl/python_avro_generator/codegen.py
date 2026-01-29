from lcdp_api import event

from avro_to_python.reader import AvscReader
from avro_to_python.writer import AvroWriter

try:
  import importlib.resources as pkg_resources
except ImportError:
  # Try backported to PY<37 `importlib_resources`.
  import importlib_resources as pkg_resources

def generate_event_classes(event_spec_directory_name, out_dir):
  with pkg_resources.path(event, event_spec_directory_name) as event_directory:
    # initialize the reader object
    reader = AvscReader(directory=event_directory)

    # generate the acyclic tree object
    reader.read()

    # initialize the writer object
    writer = AvroWriter(reader.file_tree, top_level_package="api.event.gen")

    # compile python files using 'tests/test_records as the namespace root'
    writer.write(root_dir=out_dir)

