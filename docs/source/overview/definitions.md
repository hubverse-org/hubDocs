# Key definitions

```{admonition} Modeling Hub
a consortium of research groups working together on a common set of modeling tasks, with the goal of developing ensemble models to provide stakeholders with a single model output representing uncertainty across different modeling assumptions and frameworks.
```

```{admonition} Round
a time-period for which a set of specific model outputs are solicited. Rounds define the "cadence" of submission for a modeling hub. For example, some hubs might accept daily submissions, where each day is considered a different round. Other hubs might have one round every month, with a submission period that may be open for multiple days.
```

```{admonition} Target
a quantitative outcome of interest for a modeling Hub. For example, "incident case counts". Targets typically (and sometimes implicitly) refer to a value of an observable variable in a given window of time, a given location, and possibly other stratifications (such as age group).
```

```{admonition} Task
a definition of the goals of a modeling effort, possibly including conditions, assumptions, and targets. Some tasks may be fixed across rounds, as for forecast hubs that regularly solicit predictions for a set time horizon in the near-term future. Other tasks may be more variable, as for scenario hubs that model hypothetical futures with differnt assumptions in different modeling rounds.
```

```{admonition} Team
a group of individuals developing modeling software to generate models in response to tasks coordinated by modeling hubs.
```

```{admonition} Metadata
a file or series of files that have structured information that describes general characteristics of the object they reference. For instance, model metadata files describe the characteristics of models contributing to a hub.
```

```{admonition} Schema
a declarative format used to organize and set the structure of other data including required and optional fields. Schema define the specifications for the configuration files that are required to be present in a modeling hub.
```

```{admonition} Mathematical Model formulation/structure
a statistical or mathematical formulation of a model.
```

```{admonition} Modeling software
code that implements the mathematical model formulation/structure used by a team to generate model outputs. Each team may have multiple instances of software.
```

```{admonition} Model output 
a set of target results generated in response to some modeling task for a specific round. A model might be the result of a single team’s response to the task, or it might be an ensemble of results representing outcomes of multiple efforts
```

```{admonition} Nowcast
model output that provides estimates/predictions of partially observed or unobserved values at the current date from a data stream prior to the current date. Nowcasts should be set up so that they can be evaluated for accuracy based on comparisons with the eventually observed complete data.
```

```{admonition} Forecast
a specific quantified prediction of an observable event or trend that has not yet been observed, conditional on data that has been observed up to a specified time. Forecasts should be set up so that they can be evaluated for accuracy based on comparisons with the eventual observed data.
```

```{admonition} Scenario
a description of a possible future to be modeled, described in terms of models parameters that might be varied, such as transmissibility, vaccine adoption, vaccine efficacy, the emergence of a new variant, etc.
```

```{admonition} Scenario projection
model output that provides estimates of future observations of future trends conditional on specific assumptions about a given scenario. Scenario projects are challenging to evaluate against future observed data since the assumptions under which scenarios were generated likely will never have been exactly met.
```

```{admonition} Zoltar
a research data repository that stores forecasts made by external models in standard formats and provides tools for retrieval, validation, analysis, comparison, visualization, and scoring.
```
