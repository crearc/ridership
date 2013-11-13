$(document).ready(function() {
	function Route(id, nodes){
		this.nodes = nodes;
		this.w = 400;
		this.h = 400;
		this.pad = 10;
		this.svg = d3.select("#chart-"+id)
					  .append("svg:svg")
					  .attr("width", this.w)
					  .attr("height", this.h);
	}

	Route.prototype.draw_ridership_heatmap = function() {
		var boardingscale = d3.scale.linear()
			.domain([d3.min(this.nodes, function(d) { return d.boarding; }), 
					d3.max(this.nodes, function(d) { return d.boarding; })])
			.range([0,255]);

		var alightingscale = d3.scale.linear()
			.domain([d3.min(this.nodes, function(d) { return d.alighting; }), 
					d3.max(this.nodes, function(d) { return d.alighting; })])
			.range([0,255]);

		var ridership = this.svg.selectAll("rect")
			.data(this.nodes).enter();

		var block_width = this.w / this.nodes.length;

		ridership.append("rect")
			.attr("x", function(d,i) { return i*block_width + 100; })
			.attr("width", function(d) { return block_width; })
			.style("fill", function(d) { return d3.rgb(0, boardingscale(d.boarding), 0) })
			.attr("height", 40)
			.append("svg:title")
   			.text(function(d) { return d.on_street + " and " + d.cross_street; });

		ridership.append("rect")
			.attr("y", function(d) { return 45; })
			.attr("x", function(d,i) { return i*block_width + 100; })
			.attr("width", function(d) { return block_width; })
			.style("fill", function(d) { return d3.rgb(0, alightingscale(d.alighting), 0) })
			.attr("height", 40)
			.append("svg:title")
   			.text(function(d) { return d.on_street + " and " + d.cross_street; });	

		this.svg.append("text")
		    .attr("class", "y label")
		    .attr("text-anchor", "end")
		    .attr("y", 25)
		    .attr("x", 95)
		    .attr("fill", "gray")
		    .text("Boarding");

		this.svg.append("text")
		    .attr("class", "y label")
		    .attr("text-anchor", "end")
		    .attr("y", 70)
		    .attr("x", 95)
		    .attr("fill", "gray")
		    .text("Unboarding");
	}

	Route.prototype.draw_route_map = function() {
		var xscale = d3.scale.linear()
			.domain([d3.min(this.nodes, function(d) { return d.lat; }), 
					d3.max(this.nodes, function(d) { return d.lat; })])
			.range([this.pad,this.w-this.pad]);

		var yscale = d3.scale.linear()
			.domain([d3.min(this.nodes, function(d) { return d.lng; }), 
					d3.max(this.nodes, function(d) { return d.lng; })])
			.range([this.pad,this.h-100-this.pad]);

		var colorscale = d3.scale.linear()
			.domain([d3.min(this.nodes, function(d) { return d.boarding; }), 
					d3.max(this.nodes, function(d) { return d.boarding; })])
			.range([0,255]);

		var route_map = this.svg.selectAll("circle")
			.data(this.nodes).enter();

		route_map.append("circle")
			.attr("cx", function(d) { return xscale(d.lat); })
			.attr("cy", function(d) { return yscale(d.lng)+100; })
			.attr("r", 5)
			.style("fill", function(d) { return d3.rgb(0, colorscale(d.boarding), 0) })
			.append("svg:title")
   			.text(function(d) { return d.on_street + " and " + d.cross_street; });	
	}

	function load_stop_lists() {
		var routes = $('.route-list li');
		for (var i = 0; i < routes.length; i++) {
			var route = $(routes[i]).data('route-id');
			(function(route) {
				$.getJSON( "api/routes/" + route, function( nodes ) {
					var route_map = new Route(route, nodes);
					route_map.draw_ridership_heatmap();
					route_map.draw_route_map();
				});
			})(route);
		};
	}

	load_stop_lists();

});