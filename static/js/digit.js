var points = [];
var feature_type = "a";
var fill = d3.scale.category10();
var click_started = false;
var width = 300,
    height = 400;

canvas.addEventListener('mousedown', mousedawn, false);

function mousemove (ev) {
    var x, y;

    // Get the mouse position relative to the canvas element.
    if (ev.layerX || ev.layerX == 0) { // Firefox
        x = ev.layerX;
        y = ev.layerY;
    } else if (ev.offsetX || ev.offsetX == 0) { // Opera
        x = ev.offsetX;
        y = ev.offsetY;
    }

    if (!click_started) {
        context.beginPath();
        context.moveTo(x, y);
        click_started = true;
    } else {
        context.lineTo(x, y);
        context.stroke();
    }
}




function mousedown() {
    click_started = true;
    draw_input(d3.mouse(this));
}

function mouseover() {
    if (click_started) {
        draw_input(d3.mouse(this));
    }
}

function mouseup() {
    if (click_started) {
        click_started = false;
    }
}

function draw_input(point) {
    if (point[0] < 0 || point[1] < 0 || point[0] > width || point[1] > height) {
        return;
    }
    svg.append("circle")
        .attr("r", 4)
        .attr("cx", point[0])
        .attr("cy", point[1])
        .attr("class", "dot");

    points.push(point);
}

function recognize() {
    console.log("recognize()");
}

function classify(url) {
    c = parseInt(d3.select("input#c-param").property("value"));
    if (!c) {
        c = 1;
    }
    kernel = d3.select("select#kernel-param").property("value");
    if (!kernel) {
        kernel = "gaussian";
    }
    sigma = parseInt(d3.select("input#sigma-param").property("value"));
    if (!sigma) {
        sigma = 10000;
    }
    degree = parseInt(d3.select("input#degree-param").property("value"));
    if (!degree) {
        degree = 2;
    }

    data = {
        "points": JSON.stringify(points),
        "C": JSON.stringify(c),
        "width": JSON.stringify(width),
        "height": JSON.stringify(height),
        "kernel": JSON.stringify(kernel),
        "sigma": JSON.stringify(sigma),
        "degree": JSON.stringify(degree),
    };
    request_clasify(data, url);
}

function request_clasify(message, url) {
    $.ajax({
        url:url,
        type: "GET",
        contentType: "application/json",
        dataType: 'text',
        data: message,
        success: recv,
    });
}

function clear_demo() {
    //Remove points
    svg.selectAll("circle")
        .remove();
    points = [];
}

function recv(data) {
    data = JSON.parse(data);

    if (data["status"] != "ok") {
        alert(data["status"]);
        return;
    }

    // Grid data
    z = data["z"];

    // Generate contour
    var cliff = -100;
    z.push(d3.range(z[0].length).map(function() { return cliff; }));
    z.unshift(d3.range(z[0].length).map(function() { return cliff; }));
    z.forEach(function(d) {
        d.push(cliff);
        d.unshift(cliff);
    });

    var c = new Conrec(),
        xs = d3.range(0, z.length),
        ys = d3.range(0, z[0].length),
        zs = d3.range(data["min"], data["max"], 0.1),
        x = d3.scale.linear().range([0, width]).domain([0, z.length]),
        y = d3.scale.linear().range([0, height]).domain([0, z[0].length]),
        colours = d3.scale.linear().domain(data["domain"]).range(["blue", "red"]);

    c.contour(z, 0, xs.length-1, 0, ys.length-1, xs, ys, zs.length, zs);

    // Remove old paths
    svg.selectAll("path")
        .remove();
    // Create new paths
    svg.selectAll("path").data(c.contourList())
        .enter().append("svg:path")
        .style("fill", function(d) { return colours(d.level);})
        .attr("class", "path")
        .attr("d",d3.svg.line()
            .x(function(d) { return x(d.x); })
            .y(function(d) { return y(d.y); })
        );
    // Sort points
    svg.selectAll("circle")
        .each(function(d, i) {
            this.parentNode.appendChild(this);
        });

    svg.selectAll("text")
        .each(function(d, i) {
            this.parentNode.appendChild(this);
        });

}
