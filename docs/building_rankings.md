---
title: "School Building Metrics"
---

# Seattle School Building Metrics

```js

// Load data with minor processing in python
// TODO: convert to Observable data loader
const schools = FileAttachment("data/sps-elementary-schools-clean.csv").csv({
  typed: true,
});

```

<div class="grid grid-cols-2">

  <div class="card grid-colspan-1", style="padding: 20px;">
    ${condition_swarm}

  </div>

  <div class="card grid-colspan-1", style="padding: 20px;">
    ${env_swarm}

  </div>

<div class="card grid-colspan-1", style="padding: 20px;">
    ${capacity_swarm}

  </div>

  <div class="card grid-colspan-1", style="padding: 20px;">
    ${utilization_swarm}

  </div>

</div>

```js
const condition_swarm = Plot.plot({
    title: "Building Condition",
    y: {grid: true, label: "Building Condition"},
    r: {label: "$/Student"},
    fx: {label: "Region"},
    color: {legend: false, label: "Type"},
    marks: [
        Plot.dot(schools,
            Plot.dodgeX("middle",
            {
                fx: "region",
                y: "building_condition",
                r: "budget_per_student",
                fill: "k_8",
                tip: true,
                channels: {
                        "School": "school_name",
                        },
            })),
        Plot.ruleY([62])
    ]
})
```

```js
const env_swarm = Plot.plot({
    title: "Learning Environment Assessment",
    y: {grid: true, reverse: true, label: "Learning Environment"},
    r: {label: "$/Student"},
    fx: {label: "Region"},
    color: {legend: false, label: "Type"},
    marks: [
        Plot.dot(schools,
            Plot.dodgeX("middle",
            {
                fx: "region",
                y: "learning_environment",
                r: "budget_per_student",
                fill: "k_8",
                tip: true,
                channels: {
                        "School": "school_name",
                    },
            })),
        Plot.ruleY([3.0 ])
    ]
})
```

```js
const capacity_swarm = Plot.plot({
    title: "Building Capacity",
    y: {grid: true, label: "Students/Building"},
    r: {label: "$/Student"},
    fx: {label: "Region"},
    color: {legend: false, label: "Type"},
    marks: [
        Plot.dot(schools,
            Plot.dodgeX("middle",
            {
                fx: "region",
                y: "capacity",
                r: "budget_per_student",
                fill: "k_8",
                tip: true,
                channels: {
                        "School": "school_name",
                    },
            })),
        Plot.ruleY([400])
    ]
})
```

```js
const budget_swarm = Plot.plot({
    title: "Budget per Student",
    y: {grid: true, label: "$/Student"},
    r: {label: "$/Student"},
    fx: {label: "Region"},
    color: {legend: false, label: "Type"},
    marks: [
        Plot.dot(schools,
            Plot.dodgeX("middle",
            {
                fx: "region",
                y: "budget_per_student",
                r: "budget_per_student",
                fill: "k_8",
                tip: true,
                channels: {
                        "School": "school_name",
                    },
            }))
    ]
})
```

```js
const utilization_swarm = Plot.plot({
    title: "Percent of Capacity Utilization",
    y: {grid: true, label: "Enrollment/Capacity (%)", percent: true},
    r: {label: "$/Student"},
    fx: {label: "Region"},
    color: {legend: false, label: "Type"},
    marks: [
        Plot.dot(schools,
            Plot.dodgeX("middle",
            {
                fx: "region",
                y: d => d.p223_total_count / d.capacity,
                r: "budget_per_student",
                fill: "k_8",
                tip: true,
                channels: {
                        "School": "school_name",
                    },
            })),
        Plot.ruleY([0.80])
    ]
})
```

<div class="card" style="padding: 20px;">
${rank_plot}

</div>

```js
const rank_plot = Plot.plot({
  title: "Rank of Building Metrics",
  subtitle: "Sorted by building capacity",
  x: {grid: true, axis: "top", label: "Rank", reverse: true},
  y: {tickFormat: null, ticks: 0, tickSize: 2},
  fy: {label: "School",},
  color: {domain: ["Building Condition", "Learning Environment", "Building Capacity"] , range: ["#a463f2", "#97bbf5", "#9c6b4e"], legend: true},
  width,
  marginLeft: 100,
  marks: [
    Plot.ruleY(schools, {x: 74, y: "school_name", strokeWidth: 0.1, stroke: "#cccccc"}),
    Plot.dot(schools,
      Plot.dodgeY("middle",
        {
          fy: "school_name",
          x: "capacity_rank",
          fill: "#9c6b4e",
          sort: {fy: "-x"},
          tip: true,
          channels: {
            "School": "school_name",
            "Enrollment": "p223_total_count",
            "School Capacity": "capacity",
            "School Capacity Rank": "capacity_rank",
            "Building Condition Rank": "building_condition_rank",
            "Learning Environment Rank": "learning_environment_rank"}
        },
        )),
    Plot.dot(schools,
      Plot.dodgeY("middle",
        {
          fy: "school_name",
          x: "building_condition_rank",
          fill: "#a463f2",
          symbol: "wye",
          tip: false,
        },
        )),
    Plot.dot(schools,
      Plot.dodgeY("middle",
        {
          fy: "school_name",
          x: "learning_environment_rank",
          fill: "#97bbf5",
          symbol: "cross",
          tip: false,
        },
        )),
    Plot.ruleX([54]),
    Plot.axisFy({label: null, anchor: "left", textAnchor: "end", fill: "black", tickPadding: 6})
  ]
})
```
