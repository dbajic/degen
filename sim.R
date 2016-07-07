gengraph <- function(n,m,k,show=TRUE) {
	require(igraph)
	
	print("1. degen")
	print("2. nudgen")
	choice <- readline("Choose the corresponding number of which program to run a simulation for: ")
	if (choice == 1) {
		args <- paste("degen.py",n,k,0)
	}
	else if (choice == 2) {
		args <- paste("nudegen.py",n,m,k,0)
	}
	else {
		print("Invalid choice!")
		return
	}
	graph <- as.numeric(unlist(strsplit(system2("python", args, stdout=TRUE), ",")))
	if (show) {
		plot(graph(graph, directed=FALSE), layout=layout.circle)
	}
	return(graph)
}
