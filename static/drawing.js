function writeText(cx, text, x, y) {
    cx.font = "10px Arial";
    cx.fillText(text, x, y);
}

function drawNode(cx, node, r, d) {
    cx.beginPath();
    var x = node["x"];
    var y = node["y"];
    var title = node["title"];

    cx.arc(x, y, r, 0, 2 * Math.PI);
    cx.stroke();

    writeText(cx, title, x + r + d, y + r + d);
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

function drawEdge(cx, edge, nodes, d) {
    var src_idx = edge["src"];
    var trg_idx = edge["trg"];

    var x1 = nodes[src_idx]["x"];
    var y1 = nodes[src_idx]["y"];

    var x2 = nodes[trg_idx]["x"];
    var y2 = nodes[trg_idx]["y"];
    drawArrow(cx, x1, y1, x2 + d, y2 + d);
}