d3.json("/YouTubeCA/TrendingVideos", function (projectsJson) {

	var ndx = crossfilter(projectsJson)
/*
	ndx.forEach(function(d) {
	//	d["trending_date"] = dateFormat.parse(d["trending_date"]);
	//	d["trending_date"].setDate(1);
		d["view_count"] = +d["view_count"];
		d["likes"] = +d["likes"];
		d["dislikes"] = +d["dislikes"];
		d["comment_count"] = +d["comment_count"];
	});
	*/

    var viewsDim = ndx.dimension(function(d) { return d.view_count; });
	var likesDim = ndx.dimension(function(d) { return d.likes; });
	var dislikesDim = ndx.dimension(function(d) { return d.dislikes; });
	var commentsDim = ndx.dimension(function(d) { return d.comment_count; });
	var titleDim = ndx.dimension(function(d) { return d.title; });
	var channelTitleDim = ndx.dimension(function(d) { return d.channelTitle; });

/*
    var numTitlesByViews = viewsDim.group()
    .reduceCount(function(d) {return d.view_count;});
    var numTitlesByLikes = likesDim.group()
    .reduceCount(function(d) {return d.likes;});
    var numTitlesByDislikes = dilikesDim.group()
    .reduceCount(function(d) {return d.dislikes;});
*/

	var numTitlesByViews = viewsDim.group()
	.reduceCount(function(d){return d.view_count;});
	var numTitlesByLikes = likesDim.group()
	.reduceCount(function(d){return d.likes;});
	var numTitlesByDislikes = dislikesDim.group()
	.reduceCount(function(d){return d.dislikes;});
	var titleDimgroup = titleDim.group()
	.reduceCount(function(d){return d.comment_count;});

	//Total views by videos
	var totalViewsByTitle = channelTitleDim.group().reduceSum(function (d) {
	    return d["view_count"];
	});

    //Videos by likes
	var totalLikesByTitle = titleDim.group().reduceSum(function (d) {
	    return d["likes"];
	});

	//Videos by dislikes
	var totalDislikesByTitle = titleDim.group().reduceSum(function (d) {
	    return d["dislikes"];
	});

	//var totalViewsByVideo = titleDim.group().reduceSum(function (d) {
	  //  return d["view_count"];
	//});

	var pieChart = dc.pieChart("#pie-chart");
	var row1Chart = dc.rowChart("#row-chart");
	var bubbleChart = dc.rowChart("#bubble-chart");
	var dataTable = dc.dataTable("#data-chart");

	pieChart
        .width(400)
        .height(465)
		.dimension(viewsDim)
        .group(totalViewsByTitle)
		.radius(200)
		.slicesCap(5)
        //.legend(dc.legend().x(400).y(10).itemHeight(13).gap(5));


	dataTable
        .width(960)
        .height(800)

        .dimension(titleDim)
        .group(function(d) { return d.title;
         })

        .columns([
         function(d) { return d.likes; },
         function(d) { return d.dislikes; },

          function(d) { return d.view_count; },
          function(d) { return d.comment_count; },
        ])
        .sortBy(function(d){ return d.title; })
        .order(d3.descending);


	row1Chart
        .width(700)
        .height(700)
		.dimension(likesDim)
        .group(totalLikesByTitle)
		.xAxis().tickFormat();

	bubbleChart
        .width(700)
        .height(700)
		.dimension(dislikesDim)
        .group(totalDislikesByTitle)
		.xAxis().tickFormat();


    dc.renderAll();

});