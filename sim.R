gengraph <- function(n,k,show=TRUE) {
	require(igraph)
	args <- paste("degen.py",n,k,1)
	graph <- as.numeric(unlist(strsplit(system2("python", args, stdout=TRUE), ",")))
	if (show) {
		plot(graph(graph, directed=FALSE), layout=layout.circle)
	}
	return(graph)
}
