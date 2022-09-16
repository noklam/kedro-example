# Grafana Pipeline Monitor Metrics Hook
```
class PipelineMonitoringHooks:
    def __init__(self):
        self._timers = {}
        self._client = statsd.StatsClient(prefix="kedro")

    @hook_impl
    def before_node_run(self, node: Node) -> None:
        node_timer = self._client.timer(node.name)
        node_timer.start()
        self._timers[node.short_name] = node_timer

    @hook_impl
    def after_node_run(self, node: Node, inputs: Dict[str, Any]) -> None:
        self._timers[node.short_name].stop()
        for dataset_name, dataset_value in inputs.items():
            self._client.gauge(dataset_name + "_size", sys.getsizeof(dataset_value))

    @hook_impl
    def after_pipeline_run(self):
        self._client.incr("run")
```

# DataValidationHook - Great Expectation
```python

class DataValidationHooks:
    def __init__(self) -> None:
        project_root = Path.cwd()
        # ge_contetx_root_dir = project_root / "conf" / "base" / "great_expectations"
        ge_contetx_root_dir = project_root / "great_expectations"
        self._ge_data_context = DataContext(context_root_dir=str(ge_contetx_root_dir))

    # Map expectation to dataset
    DATASET_EXPECTATION_MAPPING = {"TMIS_DATA": "tmis_dataset_expectation"}

    @hook_impl
    def before_node_run(self,node, catalog, inputs) -> None:
        """Validate inputs data to a node based on using great expectation
        if an expectation suite is defined in ``DATASET_EXPECTATION_MAPPING``.
        """
        print("Before Ndoe run")
        self._run_validation(catalog, inputs)

    @hook_impl
    def after_node_run(self, node, catalog, inputs, outputs, is_async, run_id) -> None:
        """Validate outputs data from a node based on using great expectation
        if an expectation suite is defined in ``DATASET_EXPECTATION_MAPPING``.
        """
        print("***********After Node Run:")
        self._run_validation(catalog, outputs)

    def _run_validation(self, catalog: DataCatalog, data: Dict[str, Any], run_id: str=12345):
        for dataset_name, dataset_value in data.items():
            if dataset_name not in self.DATASET_EXPECTATION_MAPPING:
                continue
            print(f"Validating dataset: {dataset_name}")
            dataset = catalog._get_dataset(dataset_name)
            dataset_path = str(dataset._filepath)
            expectation_suite = self.DATASET_EXPECTATION_MAPPING[dataset_name]

            expectation_context = ge.data_context.DataContext()
            batch = expectation_context.get_batch(
                {"path": dataset_path, "datasource": "files_datasource"}, expectation_suite,
            )
            expectation_context.run_validation_operator(
                "action_list_operator", assets_to_validate=[batch], run_id=run_id
            )
```

# AsciiDagHook
```python
# Borrow from https://github.com/iterative/dvc/blob/ee0a47f16688080457edd8bf01ae0d746d21a79e/dvc/dagascii.py
# Credit: DVC


"""Draws DAG in ASCII."""

import logging
import math
import os

from grandalf.graphs import Edge, Graph, Vertex
from grandalf.layouts import SugiyamaLayout
from grandalf.routing import EdgeViewer, route_with_lines

logger = logging.getLogger(__name__)


class VertexViewer:
    """Class to define vertex box boundaries that will be accounted for during
    graph building by grandalf.
    Args:
        name (str): name of the vertex.
    """

    HEIGHT = 3  # top and bottom box edges + text

    def __init__(self, name):
        # pylint: disable=invalid-name
        self._h = self.HEIGHT  # top and bottom box edges + text
        self._w = len(name) + 2  # right and left bottom edges + text

    @property
    def h(self):  # pylint: disable=invalid-name
        """Height of the box."""
        return self._h

    @property
    def w(self):  # pylint: disable=invalid-name
        """Width of the box."""
        return self._w


class AsciiCanvas:
    """Class for drawing in ASCII.
    Args:
        cols (int): number of columns in the canvas. Should be > 1.
        lines (int): number of lines in the canvas. Should be > 1.
    """

    TIMEOUT = 10

    def __init__(self, cols, lines):
        assert cols > 1
        assert lines > 1

        self.cols = cols
        self.lines = lines

        self.canvas = [[" "] * cols for line in range(lines)]

    def draw(self):
        """Draws ASCII canvas on the screen."""
        lines = map("".join, self.canvas)
        joined_lines = os.linesep.join(lines)
        return joined_lines

    def point(self, x, y, char):
        """Create a point on ASCII canvas.
        Args:
            x (int): x coordinate. Should be >= 0 and < number of columns in
                the canvas.
            y (int): y coordinate. Should be >= 0 an < number of lines in the
                canvas.
            char (str): character to place in the specified point on the
                canvas.
        """
        assert len(char) == 1
        assert x >= 0
        assert x < self.cols
        assert y >= 0
        assert y < self.lines

        self.canvas[y][x] = char

    def line(self, x0, y0, x1, y1, char):
        """Create a line on ASCII canvas.
        Args:
            x0 (int): x coordinate where the line should start.
            y0 (int): y coordinate where the line should start.
            x1 (int): x coordinate where the line should end.
            y1 (int): y coordinate where the line should end.
            char (str): character to draw the line with.
        """
        # pylint: disable=too-many-arguments, too-many-branches
        if x0 > x1:
            x1, x0 = x0, x1
            y1, y0 = y0, y1

        dx = x1 - x0
        dy = y1 - y0

        if dx == 0 and dy == 0:
            self.point(x0, y0, char)
        elif abs(dx) >= abs(dy):
            for x in range(x0, x1 + 1):
                if dx == 0:
                    y = y0
                else:
                    y = y0 + int(round((x - x0) * dy / float(dx)))
                self.point(x, y, char)
        elif y0 < y1:
            for y in range(y0, y1 + 1):
                if dy == 0:
                    x = x0
                else:
                    x = x0 + int(round((y - y0) * dx / float(dy)))
                self.point(x, y, char)
        else:
            for y in range(y1, y0 + 1):
                if dy == 0:
                    x = x0
                else:
                    x = x1 + int(round((y - y1) * dx / float(dy)))
                self.point(x, y, char)

    def text(self, x, y, text):
        """Print a text on ASCII canvas.
        Args:
            x (int): x coordinate where the text should start.
            y (int): y coordinate where the text should start.
            text (str): string that should be printed.
        """
        for i, char in enumerate(text):
            self.point(x + i, y, char)

    def box(self, x0, y0, width, height):
        """Create a box on ASCII canvas.
        Args:
            x0 (int): x coordinate of the box corner.
            y0 (int): y coordinate of the box corner.
            width (int): box width.
            height (int): box height.
        """
        assert width > 1
        assert height > 1

        width -= 1
        height -= 1

        for x in range(x0, x0 + width):
            self.point(x, y0, "-")
            self.point(x, y0 + height, "-")

        for y in range(y0, y0 + height):
            self.point(x0, y, "|")
            self.point(x0 + width, y, "|")

        self.point(x0, y0, "+")
        self.point(x0 + width, y0, "+")
        self.point(x0, y0 + height, "+")
        self.point(x0 + width, y0 + height, "+")


def _build_sugiyama_layout(vertices, edges):
    #
    # Just a reminder about naming conventions:
    # +------------X
    # |
    # |
    # |
    # |
    # Y
    #

    vertices = {v: Vertex(f" {v} ") for v in vertices}
    # NOTE: reverting edges to correctly orientate the graph
    edges = [Edge(vertices[e], vertices[s]) for s, e in edges]
    vertices = vertices.values()
    graph = Graph(vertices, edges)

    for vertex in vertices:
        vertex.view = VertexViewer(vertex.data)

    # NOTE: determine min box length to create the best layout
    minw = min(v.view.w for v in vertices)

    for edge in edges:
        edge.view = EdgeViewer()

    sug = SugiyamaLayout(graph.C[0])
    graph = graph.C[0]
    roots = list(filter(lambda x: len(x.e_in()) == 0, graph.sV))

    sug.init_all(roots=roots, optimize=True)

    sug.yspace = VertexViewer.HEIGHT
    sug.xspace = minw
    sug.route_edge = route_with_lines

    sug.draw()

    return sug


def draw(vertices, edges):
    """Build a DAG and draw it in ASCII.
    Args:
        vertices (list): list of graph vertices.
        edges (list): list of graph edges.
    """
    # pylint: disable=too-many-locals
    # NOTE: coordinates might me negative, so we need to shift
    # everything to the positive plane before we actually draw it.
    Xs = []  # pylint: disable=invalid-name
    Ys = []  # pylint: disable=invalid-name

    sug = _build_sugiyama_layout(vertices, edges)

    for vertex in sug.g.sV:
        # NOTE: moving boxes w/2 to the left
        Xs.append(vertex.view.xy[0] - vertex.view.w / 2.0)
        Xs.append(vertex.view.xy[0] + vertex.view.w / 2.0)
        Ys.append(vertex.view.xy[1])
        Ys.append(vertex.view.xy[1] + vertex.view.h)

    for edge in sug.g.sE:
        for x, y in edge.view._pts:  # pylint: disable=protected-access
            Xs.append(x)
            Ys.append(y)

    minx = min(Xs)
    miny = min(Ys)
    maxx = max(Xs)
    maxy = max(Ys)

    canvas_cols = int(math.ceil(math.ceil(maxx) - math.floor(minx))) + 1
    canvas_lines = int(round(maxy - miny))

    canvas = AsciiCanvas(canvas_cols, canvas_lines)

    # NOTE: first draw edges so that node boxes could overwrite them
    for edge in sug.g.sE:
        # pylint: disable=protected-access
        assert len(edge.view._pts) > 1
        for index in range(1, len(edge.view._pts)):
            start = edge.view._pts[index - 1]
            end = edge.view._pts[index]

            start_x = int(round(start[0] - minx))
            start_y = int(round(start[1] - miny))
            end_x = int(round(end[0] - minx))
            end_y = int(round(end[1] - miny))

            assert start_x >= 0
            assert start_y >= 0
            assert end_x >= 0
            assert end_y >= 0

            canvas.line(start_x, start_y, end_x, end_y, "*")

    for vertex in sug.g.sV:
        # NOTE: moving boxes w/2 to the left
        x = vertex.view.xy[0] - vertex.view.w / 2.0
        y = vertex.view.xy[1]

        canvas.box(
            int(round(x - minx)),
            int(round(y - miny)),
            vertex.view.w,
            vertex.view.h,
        )

        canvas.text(
            int(round(x - minx)) + 1, int(round(y - miny)) + 1, vertex.data
        )

    return canvas.draw()
    
class AsciiHook:
    def _get_pipeline_graph(self, pipeline):
        edges = []

        for node in pipeline.nodes:
            name = f"{node.short_name}"
            for input_ in node.inputs:
                edges.append((input_, name))
            for output_ in node.outputs:
                edges.append((name, output_))
        return edges

    def draw_graph(self, edges, vertexes=None, reverse=True):
        if vertexes is None:
            vertexes = set(itertools.chain(*edges))  # find unique nodes
        if reverse:
            print(edges)
            edges = [(e[1], e[0]) for e in edges]  # Reverse the drawing direction

        print(draw(vertexes, edges))

    def draw_pipeline(self, pipeline):
        graph = self._get_pipeline_graph(pipeline)
        self.draw_graph(graph)

    @hook_impl
    def before_pipeline_run(self, pipeline):
        self.draw_pipeline(pipeline)
```

# RichLogRecorderHook
```python
from rich import reconfigure
from rich import get_console

class RichLogRecorderHook:
    @hook_impl
    def after_context_created(self):
        reconfigure(record=True)

    @hook_impl
    def after_pipeline_run(self):
        # get_console().save_html("logs.html")  # Would save the HTML instead
        get_console().save_text("logs.text")  # Save the text version 
 ```
