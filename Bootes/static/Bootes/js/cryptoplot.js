var margin = {top: 30, right: 20, bottom: 30, left: 100},
    width = 600 - margin.left - margin.right,
    height = 300 - margin.top - margin.bottom;

function DataPlotter(lineData){

    var yScale = d3.scaleLinear()
        .domain(d3.extent(lineData.map(function(d) { return d.y; })))
        .range([height,0]);

    var xScale = d3.scaleTime()
        .domain(d3.extent(lineData.map(function(d) { return d.x; })))
        .range([0,width]);

    var xAxis = d3.axisBottom(xScale)
        .ticks(10);

    var yAxis = d3.axisLeft(yScale)
        .ticks(10);

    var svgContainer = d3.select('#DataContent')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    var bisectDate = d3.bisector(function(d) {return d.x; }).left,
        formatValue = d3.format(',.2f'),
        formatCurrency = function(d) {return '$' + formatValue(d); };

    svgContainer.append('g')
        .attr('class', 'axis')
        .attr('transform', 'translate(' + (width/8) + ',' + (height+margin.top) + ')')
        .call(xAxis);

    svgContainer.append('text')
        .attr('y', 160)
        .attr('x', 30)
        .attr('transform', 'rotate(90)')
        .style('text-anchor', 'middle')
        .text('Price ($)')

    svgContainer.append('g')
        .attr('class', 'axis')
        .attr('transform', 'translate( ' + (width/8) + ',' + margin.top + ')')
        .call(yAxis);

    var lineFunction = d3.line()
            .curve(d3.curveLinear)
            .x(function(d) { return xScale(d.x); })
            .y(function(d) { return yScale(d.y); });

    svgContainer.append("path")
        .attr('class', 'cryptoline')
        .attr('transform', 'translate( ' + (width/8) + ',' + margin.top + ')')
        .attr("d", lineFunction(lineData))
        .attr(lineFunction);

    var focus = svgContainer.append("g")
        .attr("class", "focus")
        .style("display", "none");

    focus.append("circle")
        .attr('transform', 'translate( ' + (width/8) + ',' + margin.top + ')')
        .attr("r", 4.5);

    focus.append("text")
        .attr('transform', 'translate( ' + (width/8) + ',' + margin.top + ')')
        .attr("x", 9)
        .attr("dy", ".35em");

    var intplt1 = svgContainer.append("rect")
        .attr("class", "overlay")
        .attr("width", width)
        .attr("height", height)
        .attr('transform', 'translate( ' + (width/8) + ',' + margin.top + ')')
        .attr('fill', 'transparent')
        .on("mouseover", function() { focus.style("display", null); })
        .on("mouseout", function() { focus.style("display", "none"); })
        .on("mousemove", mousemove);

    function mousemove() {
      var x0 = xScale.invert(d3.mouse(this)[0]),
          i = bisectDate(lineData, x0, 1),
          d0 = lineData[i - 1],
          d1 = lineData[i],
          d = x0 - d0.x > d1.x - x0 ? d1 : d0;
    focus.attr('transform', 'translate(' + xScale(d.x) + ',' + yScale(d.y) + ')');
      //focus.attr("transform", "translate(" + xScale(d.x) + "," + yScale(d.y) + ")");
      focus.select("text").text(formatCurrency(d.y));
  }
}
