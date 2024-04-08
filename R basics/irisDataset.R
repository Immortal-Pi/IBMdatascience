library(datasets,ggplot2)
data(iris)
View(iris)
ggplot(iris,aes(x=Sepal.Length,y=Sepal.Width))+geom_point()
