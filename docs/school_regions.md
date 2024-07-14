
# Well-Resourced Schools

## By SPS Region

```js
// Load raw data
const schools_raw = FileAttachment("data/sps-elementary-schools.csv").csv({
  typed: true,
});

// Load data with minor processing in python
// TODO: convert to Observable data loader
const schools = FileAttachment("data/sps-elementary-schools-clean.csv").csv({
  typed: true,
});

const map = FileAttachment("data/geo/sps_attendance_area_ES.geojson").json();
const es_boundaries = FileAttachment("data/geo/Elementary_School_Attendance_Areas_2023-2024.geojson").json();
const ms_boundaries = FileAttachment("data/geo/Middle_School_Attendance_Areas_2023-2024.geojson").json();
```

```js
// function sparkbar(max) {
//   return (x) => htl.html`<div style="
//     background: var(--theme-green);
//     color: black;
//     font: 10px/1.6 var(--sans-serif);
//     width: ${100 * x / max}%;
//     float: right;
//     padding-right: 3px;
//     box-sizing: border-box;
//     overflow: visible;
//     display: flex;
//     justify-content: end;">${x.toLocaleString("en-US")}`
// }

function sparkbar(max) {
  return (x) => {
    // Calculate the percentage of x relative to max
    const percentage = x / max;

    // Calculate the color based on the percentage
    const red = Math.round(255 * (1 - percentage));
    const green = Math.round(255 * percentage);

    return htl.html`<div style="
      background: rgb(${red}, ${green}, 100);
      color: black;
      font: 10px/1.6 var(--sans-serif);
      width: ${100 * x / max}%;
      float: right;
      padding-right: 3px;
      box-sizing: border-box;
      overflow: visible;
      display: flex;
      justify-content: end;">${x.toLocaleString("en-US")}</div>`
  }
};

function sparkbarRev(max) {
  return (x) => {
    // Calculate the percentage of x relative to max
    const percentage = x / max;

    // Calculate the color based on the percentage (reversed from sparkbar)
    const green = Math.round(255 * (1 - percentage));
    const red = Math.round(255 * percentage);

    return htl.html`<div style="
      background: rgb(${red}, ${green}, 100);
      color: black;
      font: 10px/1.6 var(--sans-serif);
      width: ${100 * x / max}%;
      float: right;
      padding-right: 3px;
      box-sizing: border-box;
      overflow: visible;
      display: flex;
      justify-content: end;">${x.toLocaleString("en-US")}</div>`
  }
};

function sparkbarSimple(max) {
  return (x) => {
    // Calculate the percentage of x relative to max
    const percentage = x / max;

    // Calculate the color based on the percentage (reversed from sparkbar)
    const green = Math.round(255 * (1 - percentage));
    const red = Math.round(255 * percentage);

    return htl.html`<div style="
      background: currentBackgroundColor;
      color: black;
      font: 10px/1.6 var(--sans-serif);
      width: ${100 * percentage}%;
      float: right;
      padding-right: 3px;
      box-sizing: border-box;
      overflow: visible;
      display: flex;
      justify-content: end;">${x.toLocaleString("en-US")}</div>`
  }
};
```

Select the region to focus dashboards on:

```js
const schoolsRegion = view(
  Inputs.select(
    d3.group(schools, (d) => d.region),
    {label: "SPS Region", key: ["Northwest", "Northeast", "Central", "Southwest", "Southeast"]}
  )
);
```

```js
view(Inputs.table(schoolsRegion.flat(), {
  columns: [
    "school",
    // "k_8",
    "building_condition",
    "learning_environment",
    "capacity",
    "p223_k5_count",
    // "total_budget",
    // "budget_per_k8_student",
  ],
  format: {
    "building_condition": sparkbar(d3.max(schoolsRegion.flat(), d => d.building_condition)),
    "learning_environment": sparkbarRev(d3.max(schoolsRegion.flat(), d => d.learning_environment)),
    "capacity": sparkbar(d3.max(schoolsRegion.flat(), d => d.capacity)),
    "building_condition_rank": sparkbar(d3.max(schoolsRegion.flat(), d => d.building_condition_rank)),
    "learning_environment_rank": sparkbar(d3.max(schoolsRegion.flat(), d => d.learning_environment_rank)),
    "capacity_rank": sparkbar(d3.max(schoolsRegion.flat(), d => d.capacity_rank)),
    "p223_k5_count": sparkbar(d3.max(schoolsRegion.flat(), d => d.p223_k5_count)),
    // "total_budget": (value) => {
    //   const formattedValue = '$' + value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    //   return sparkbar(d3.max(schoolsRegion.flat(), d => d.budget))(formattedValue);
    // },
    // "budget_per_k8_student": (value) => {
    //   const formattedValue = '$' + value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    //   return sparkbar(d3.max(schoolsRegion.flat(), d => d.budget))(formattedValue);
    // },
  },
  header: {
    school: "School",
    // k_8: "Grades",
    building_condition: "Bldg. Condition",
    learning_environment: "Learning Env.",
    capacity: "Bldg. Capacity",
    p223_k5_count: "K5 Enrollment",
    // total_budget: "Total Budget",
    // budget_per_k8_student: "$/Student",
  }
}))
```

```js
Plot.plot({
    title: "Relationship across building resource metrics",
    nice: true,
    y: {grid: true, reverse: true, label: "Learning Environment (Rank)"},
    x: {grid: true, reverse: true, label: "Building Condition (Rank)"},
    r: {label: "Enrollment (June 2024)"},
    symbol: {label: "K-8", legend: true},
    color: {label: "Building Capacity", legend: true,
          scheme: "Cool"
    },
    marks: [
      Plot.text([{x: 80, y: 80, text: "Low Building Condition & Low Learning Environment"}]),
      Plot.dot(schoolsRegion.flat(),
        {
          x: "building_condition_rank",
          y: "learning_environment_rank",
          fill: "capacity",
          r: "p223_k5_count",
          symbol: "k_8",
          tip: {
          format: {
            school: true,
            building_condition: true,
            learning_environment: true,
            budget_per_k8_student: true,
            r: false,
            y: false,
            x: false,
            symbol: false,
            fill: false
          }
          },
          channels: {
                    "School": "school",
                    "2023/24 Enrollment": "p223_total_count",
                    "Learning Environment": "learning_environment",
                    "Building Condition": "building_condition",
                    "School Capacity": "capacity",
                    "$/Student": "budget_per_k8_student",
                    },}
        ),
        Plot.ruleX([50]),
        Plot.ruleY([50])]
                })
```

```js
Plot.plot({
    title: "Distance to Nearest Schools",
    nice: true,
    x: {grid: true, reverse: false, label: "Distance to Nearest Elementary (miles)"},
    y: {grid: true, reverse: false, label: "Building Capacity"},
    r: {label: "Enrollment (June 2024)"},
    symbol: {label: "K-8", legend: true},
    color: {label: "Region", legend: true},
    marks: [
      Plot.dot(schoolsRegion.flat(),
        {
          x: "distance_to_nearest_school",
          y: "capacity",
          fill: "region",
          r: "p223_k5_count",
          symbol: "k_8",
          tip: {
          format: {
            school: true,
            capacity: true,
            r: false,
            y: false,
            x: false,
            symbol: false,
            fill: false,
          }
          },
          channels: {
                    "School": "school",
                    "Building Capacity": "capacity",
                    "Enrollment": "p223_k5_count",
                    "Nearest School": "nearest_school",
                    "Distance (miles)": "distance_to_nearest_school",
                    },}
        ),
        Plot.ruleY([450]),
        ], caption: "Note: Size of each point is determined by K-5 enrollment as of June 2024."
                })
```

```js
Plot.plot({
    title: "Relationship between budget and enrollment",
    nice: true,
    y: {grid: true, label: "Total Budget"},
    x: {grid: true, label: "K-8 Enrollment (June 2024)"},
    symbol: {label: "K-8", legend: true, legendTitle: "Color Legend Title"},
    color: {label: "Building Capacity", legend: true,
          scheme: "Cool"
    },
    marginLeft: 50,
    marks: [Plot.dot(schoolsRegion.flat(),
        {
          x: "p223_k8_count",
          y: "total_budget",
          r: "budget_per_k8_student",
          fill: "capacity",
          symbol: "k_8",
          tip: {
          format: {
            school: true,
            building_condition: true,
            learning_environment: true,
            budget_per_k8_student: true,
            r: false,
            y: false,
            x: false,
            symbol: false,
            fill: false
          }
          },
          channels: {
                    "School": "school",
                    "Building Capacity": "capacity",
                    "K-5 Enrollment (June 2024)": "p223_k5_count",
                    "K-8 Enrollment (June 2024)": "p223_k8_count",
                    "$ per K-8 Student": "budget_per_k8_student",
                    },}
        ),],
        caption: "Note: Size of each point is the budget per K-8 student."
                })
```

```js
Plot.plot({
  title: "School administrative budget per student (2024)",
  x: {label: "$/Student", tickPadding: 6, tickSize: 0, axis: "top",},
  y: {label: null, tickSize: 0},
  color: {label: "Building Capacity", legend: true,
          scheme: "Cool"
    },
  marginLeft: 100,
  marks: [
    Plot.ruleY(schoolsRegion.flat(), {x: "budget_per_k8_student", y: "school", stroke: "capacity", strokeWidth: 2}),
    Plot.ruleX(schoolsRegion.flat(), {x: 5507.9259, strokeWidth: 2}),
    Plot.dot(schoolsRegion.flat(), {
          x: "budget_per_k8_student",
          y: "school",
          symbol: "k_8",
          fill: "capacity",
          r: 4,
          sort: {y: "-x"},
          tip: {
          format: {
            r: true,
            y: true,
            x: true,
            symbol: true,
            p223_k5_count: true,
          }
        },
    channels: {
              "Enrollment (June 2024)": "p223_k5_count",
              },
    } )
  ], caption: "Note: K-8 schools budget per student account for the total K-8 P223 enrollment as of June 2024, where as K-5 per student costs are based on total K-5 P223 enrollment."
})
```
