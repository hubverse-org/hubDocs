# History  

```{margin}
Reich, N. G., Lessler, J., Funk, S., Viboud, C., Vespignani, A., Tibshirani, R. J., ... & Biggerstaff, M. (2022). [Collaborative hubs: making the most of predictive epidemic modeling](https://ajph.aphapublications.org/doi/full/10.2105/AJPH.2022.306831). *American journal of public health*, 112(6), 839-842.
```

```{admonition} Reference
This [short paper on collaborative hubs] (https://ajph.aphapublications.org/doi/full/10.2105/AJPH.2022.306831) provides a thorough discussion of forecasting hubs for infectious diseases, including the reasoning behind them.  
```

In the early 2010s, there were many infectious disease forecasting models, but most were published months to years after the forecasted event. These models often had very different targets they were forecasting, such as weekly incidence, epidemic duration, monthly visits, and time of peak incidence. Additionally, the accuracy of these models was evaluated using very different metrics, such as the mean absolute error, median absolute error, and correlation. These factors made comparing forecast models fairly, consistently, and accurately very challenging. In a scoping review of influenza forecasting in human populations published in 2014, Chretien et al. concluded that:  

```{margin}
Chretien, J. P., George, D., Shaman, J., Chitale, R. A., & McKenzie, F. E. (2014). [Influenza forecasting in human populations: a scoping review](https://pubmed.ncbi.nlm.nih.gov/24714027/). *PloS one*, 9(4), e94130.
```

```{epigraph}
"Comparing the accuracy of forecasting applications is difficult because forecasting methods, forecast outcomes, and reported validation metrics varied widely."  
```

At the same time, various efforts were made to aggregate and evaluate forecasts for infectious diseases to better address the challenges they pose from a public health perspective. Below is a timeline of some of the major "hubs" developed since 2013.  

## Timeline showing various major infectious disease forecasting "hubs"  
```{figure} ../images/hub-timeline.png
---
figclass: margin-caption
alt: A timeline indicating the years when various major infectious disease forecasting hubs have been active.
name: hub-timeline
---
Figure credits: Alex Vespignani and Nicole Samay. 
```

The hubverse provides tools and a unified framework for aggregating, visualizing, and evaluating forecasts. Although infectious disease forecasting motivated the development of these tools, the approach is meant to be versatile so that the hubverse can be used for other types of forecasts.  

# Motivation  

There are many reasons to support collaborative modeling rather than relying on a single forecasting model. Firstly, ensemble models are both more accurate and useful than individual models:  
- A simple average across models has better predictive performance  
- Ensemble models are especially reliable for predicting across multiple targets  

Additionally, there are scientific and structural benefits to modeling via hubs:  
- They allow comparable evaluation across different models  
- They provide opportunities for scientific exchange and for method & data sharing  
- Hubs have a greater transparency of model outputs  
- Hubs can also be a venue for communication with stakeholders  

In working on collaborative forecasting, our principal objectives have been to  
- Connect forecasting research to decision-making needs  
- Evaluate forecast skills and facilitate forecasting research  
- Operationalize forecasting
- Ensure increased data availability and real-time forecasting  
- Forecast and evaluation standardization  
- Community building (e.g., CSTE, academia, industry)  
- Aggregate and coordinate the work done by varied forecasting teams  

