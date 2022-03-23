function drawNodes(cx, graph_dict) {
    for (var j = 0; j < graph_dict["nodes"].length; j++) {
        var node = graph_dict["nodes"][j];
        cx.beginPath();
        cx.arc(parseInt(node["x"], 10), parseInt(node["y"], 10), 2, 0, 2 * Math.PI);
        cx.stroke();

        cx.font = "10px Arial";
        cx.fillText(node["title"], node["x"] + 5, node["y"] + 5);
    }
}

function drawEdges(cx, graph_dict) {
    for (var j = 0; j < graph_dict["edges"].length; j++) {
        var edge = graph_dict["edges"][j];
        var src_idx = parseInt(edge["src"], 10);
        var trg_idx = parseInt(edge["trg"], 10);

        var fromx = parseInt(graph_dict["nodes"][src_idx]["x"], 10);
        var fromy = parseInt(graph_dict["nodes"][src_idx]["y"], 10);

        var tox = parseInt(graph_dict["nodes"][trg_idx]["x"], 10);
        var toy = parseInt(graph_dict["nodes"][trg_idx]["y"], 10);
        drawArrow(cx, fromx, fromy, tox, toy);
    }
}

function drawArrow(cx, x1, y1, x2, y2) {
    var headlen = 5;
    var dx = x2 - x1;
    var dy = y2 - y1;
    var angle = Math.atan2(dy, dx);
    cx.beginPath()
    cx.moveTo(x1, y1);
    cx.lineTo(x2, y2);
    cx.lineTo(x2 - headlen * Math.cos(angle - Math.PI / 6), y2 - headlen * Math.sin(angle - Math.PI / 6));
    cx.moveTo(x2, y2);
    cx.lineTo(x2 - headlen * Math.cos(angle + Math.PI / 6), y2 - headlen * Math.sin(angle + Math.PI / 6));
    cx.stroke();
}