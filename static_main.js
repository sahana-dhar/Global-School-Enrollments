d3.csv('project_modified.csv').then(data => {
    data.forEach(d => {
      d['Educational attainment, at least completed lower secondary, population 25+, total (%) (cumulative)'] = +d['Educational attainment, at least completed lower secondary, population 25+, total (%) (cumulative)'];
      d['Year'] = +d['Year'];
    });
  
    const averageEnrollmentByYear = d3.rollup(data, 
      v => d3.mean(v, d => d['Educational attainment, at least completed lower secondary, population 25+, total (%) (cumulative)']), 
      d => d.Year);
  
    const averageEnrollmentArray = Array.from(averageEnrollmentByYear, ([Year, enrollmentRate]) => ({ Year, enrollmentRate }));   

    const EnrollmentArray = averageEnrollmentArray.filter(d => d.Year !== 2023);
  
    const svgTrend = d3.select("#trendlineSVG"),
            margin = { top: 20, right: 20, bottom: 50, left: 50 },
            width = +svgTrend.attr("width") - margin.left - margin.right,
            height = +svgTrend.attr("height") - margin.top - margin.bottom;
  
    const x = d3.scaleTime().range([0, width]);
    const y = d3.scaleLinear().range([height, 0]);
  
    const g = svgTrend.append("g").attr("transform", `translate(${margin.left},${margin.top})`);
  
    const formattedData = EnrollmentArray.map(d => ({
      year: new Date(d.Year, 0),
      enrollmentRate: d.enrollmentRate
    }));
  
    x.domain(d3.extent(formattedData, d => d.year));
    y.domain([0, d3.max(formattedData, d => d.enrollmentRate)]);
  
    const valueline = d3.line()
    .x(d => x(d.year))
    .y(d => y(d.enrollmentRate));

    g.append("path")
        .data([formattedData])
        .attr("class", "line")
        .attr("d", valueline)
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 2);

    g.selectAll(".dot")
        .data(formattedData)
        .enter().append("circle")
        .attr("class", "dot")
        .attr("cx", d => x(d.year))
        .attr("cy", d => y(d.enrollmentRate))
        .attr("r", 5)
        .attr("fill", "steelblue");
  
    g.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x));
  
    g.append("g").call(d3.axisLeft(y));

    const xAxis = g.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x));

    const yAxis = g.append("g")
        .call(d3.axisLeft(y));

    xAxis.append("text")
        .attr("fill", "#000")
        .attr("transform", `translate(${width / 2}, ${margin.bottom -10})`) 
        .style("text-anchor", "middle")
        .style("font-size", "15px")
        .text("Year");

    yAxis.append("text")
        .attr("fill", "#000")
        .attr("transform", `rotate(-90) translate(${-height / 2},0)`)
        .attr("y", -margin.left + 20)
        .attr("text-anchor", "middle")
        .style("font-size", "15px")
        .text("Average Educational Attainment Rate (%)");
  });

d3.csv('project_modified.csv').then(data => {
    let maleRates = [];
    let femaleRates = [];

    data.forEach(d => {
        const maleRate = parseFloat(d['Educational attainment, at least completed lower secondary, population 25+, male (%) (cumulative)']);
        const femaleRate = parseFloat(d['Educational attainment, at least completed lower secondary, population 25+, female (%) (cumulative)']);

        if (isFinite(maleRate)) maleRates.push(maleRate);
        if (isFinite(femaleRate)) femaleRates.push(femaleRate);
    });

    function calculateStatistics(dataArray) {
        dataArray.sort(d3.ascending);
        let q1 = d3.quantile(dataArray, 0.25);
        let median = d3.quantile(dataArray, 0.5);
        let q3 = d3.quantile(dataArray, 0.75);
        let min = dataArray[0];
        let max = dataArray[dataArray.length - 1]
        return { q1, median, q3, min, max };
    }

    let maleStats = calculateStatistics(maleRates);
    let femaleStats = calculateStatistics(femaleRates);

    drawBoxplot(maleStats, "Male");
    drawBoxplot(femaleStats, "Female");

    gBoxplot.append("g")
        .attr("transform", `translate(0,${heightBoxplot})`)
        .call(d3.axisBottom(xScaleBoxplot));

    gBoxplot.append("g").call(d3.axisLeft(yScaleBoxplot));

    gBoxplot.append("text")
        .attr("fill", "#000")
        .attr("transform", `translate(${widthBoxplot / 2}, ${marginBoxplot.bottom + 310})`) 
        .style("text-anchor", "middle")
        .style("font-size", "15px")
        .text("Gender");

    gBoxplot.append("text")
        .attr("fill", "#000")
        .attr("transform", `rotate(-90) translate(${-heightBoxplot / 2},0)`)
        .attr("y", -marginBoxplot.left + 20)
        .attr("text-anchor", "middle")
        .style("font-size", "15px")
        .text("Educational Attainment Rate (%)");
});

const svgBoxplot = d3.select("#boxplotSVG"),
      marginBoxplot = { top: 20, right: 20, bottom: 50, left: 100 },
      widthBoxplot = +svgBoxplot.attr("width") - marginBoxplot.left - marginBoxplot.right,
      heightBoxplot = +svgBoxplot.attr("height") - marginBoxplot.top - marginBoxplot.bottom;

const gBoxplot = svgBoxplot.append("g").attr("transform", `translate(${marginBoxplot.left},${marginBoxplot.top})`);

const yScaleBoxplot = d3.scaleLinear()
    .range([heightBoxplot, 0])
    .domain([0, 100]);

const xScaleBoxplot = d3.scaleBand()
    .range([0, widthBoxplot])
    .domain(["Male", "Female"])
    .padding(0.2);

const drawBoxplot = (data, gender) => {
    const x = xScaleBoxplot(gender);
    const y1 = yScaleBoxplot(data.q3);
    const y2 = yScaleBoxplot(data.q1);
    const medianY = yScaleBoxplot(data.median);
    const minY = yScaleBoxplot(data.min);
    const maxY = yScaleBoxplot(data.max);

    gBoxplot.append("rect")
        .attr("x", x)
        .attr("y", y1)
        .attr("width", xScaleBoxplot.bandwidth())
        .attr("height", y2 - y1)
        .attr("fill", gender === "Male" ? "lightblue" : "pink");

    gBoxplot.append("line")
        .attr("x1", x)
        .attr("x2", x + xScaleBoxplot.bandwidth())
        .attr("y1", medianY)
        .attr("y2", medianY)
        .attr("stroke", "red")
        .attr("stroke-width", 2);

    gBoxplot.append("line")
        .attr("x1", x + xScaleBoxplot.bandwidth() / 2)
        .attr("x2", x + xScaleBoxplot.bandwidth() / 2)
        .attr("y1", minY)
        .attr("y2", y2)
        .attr("stroke", "black");

    gBoxplot.append("line")
        .attr("x1", x + xScaleBoxplot.bandwidth() / 2)
        .attr("x2", x + xScaleBoxplot.bandwidth() / 2)
        .attr("y1", maxY)
        .attr("y2", y1)
        .attr("stroke", "black");

    gBoxplot.append("circle")
        .attr("cx", x + xScaleBoxplot.bandwidth() / 2)
        .attr("cy", minY)
        .attr("r", 3)
        .attr("fill", "black");

    gBoxplot.append("circle")
        .attr("cx", x + xScaleBoxplot.bandwidth() / 2)
        .attr("cy", maxY)
        .attr("r", 3)
        .attr("fill", "black");
};