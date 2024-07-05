
# Well-Resourced Schools

## Sharing Data on Seattle Public Elementary Schools


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

<div class="grid grid-cols-4">

  <div class="card grid-colspan-2 grid-rowspan-2", style="padding: 20px;">
    ${school_map}

  </div>

  <div class="card grid-colspan-1"">

  <div id="container" style="border-radius: 8px; overflow: hidden; margin: 0rem 0;">
  ${school_scatter}

  </div>

  </div>

  <div class="card grid-colspan-1"">

  <div id="container" style="border-radius: 8px; overflow: hidden; margin: 0rem 0;">
  ${budget_scatter}

  </div>

  </div>

</div>

<!-- Create interactive map -->

```js
const school_map = Plot.plot({
    title: "SPS Elementary School Locations",
    subtitle: "Size of points indicates relative budget per student",
    projection: {
      type: "mercator",
      domain: es_boundaries // Automatically fits the map to Seattle's boundaries
    },
    r: {label: "$/Student"},
    symbol: {label: "Type", legend: true},
    color: {legend: true,
      range: ["#4269d0", "#ff725c"]
    },
    width,
    marks: [
      Plot.geo(es_boundaries, {
        stroke: "#9498a0",
        strokeWidth: 0.5
      }),
      Plot.geo(ms_boundaries, {
        stroke: "#000000",
        strokeWidth: 1.0
      }),
      Plot.dot(schools, {
        x: "longitude",
        y: "latitude",
        r: "budget_per_student",
        // stroke: "highly_capable",
        symbol: "option_school",
        fill: (d) => d.capacity > 400 ? "Capacity greater than 400" : "Capacity less than 400",
        tip: {
          format: {
            school_name: true,
            building_condition: true,
            learning_environment: true,
            budget_per_student: true,
            r: false,
            y: false,
            x: false,
            symbol: false,
            fill: false
          }
        },
        channels: {
                    "School": "school_name",
                    "Building Condition": "building_condition",
                    "Learning Environment": "learning_environment",
                    "Building Capacity": "capacity",
                    "Enrollment": "p223_total_count",
                    "$/Student": "budget_per_student",
                    },
      })
    ]
  })
```

```js
const school_scatter = Plot.plot({
    title: "Relationship across building resource metrics",
    nice: true,
    y: {grid: true, reverse: true, label: "Learning Environment Rank"},
    x: {grid: true, reverse: true, label: "Building Condition Rank"},
    r: {label: "Budget per Student"},
    symbol: {label: "K-8", legend: true},
    color: {label: "School Size", legend: true,
      range: ["#4269d0", "#ff725c"]
    },
    marks: [Plot.dot(schools,
        {
          x: "building_condition_rank",
          y: "learning_environment_rank",
          fill: (d) => d.capacity > 400 ? "Capacity greater than 400" : "Capacity less than 400",
          r: "budget_per_student",
          symbol: "k_8",
          tip: {
          format: {
            school_name: true,
            building_condition: true,
            learning_environment: true,
            budget_per_student: true,
            r: false,
            y: false,
            x: false,
            symbol: false,
            fill: false
          }
          },
          channels: {
                    "School": "school_name",
                    "2023/24 Enrollment": "p223_total_count",
                    "Learning Environment": "learning_environment",
                    "Building Condition": "building_condition",
                    "School Capacity": "capacity",
                    "$/Student": "budget_per_student",
                    },}
        ),
        Plot.ruleX([50]),
        Plot.ruleY([50])]
                })
```

```js
const budget_scatter = Plot.plot({
    title: "Relationship between budget and enrollment",
    nice: true,
    y: {grid: true, label: "Total Budget"},
    x: {grid: true, label: "2023/24 Enrollment"},
    r: {label: "Budget per Student"},
    symbol: {label: "K-8", legend: true, legendTitle: "Color Legend Title"},
    color: {legend: true,
      range: ["#4269d0", "#ff725c"]
    },
    marks: [Plot.dot(schools,
        {
          x: "p223_total_count",
          y: "total_budget",
          fill: (d) => d.capacity > 400 ? "Capacity greater than 400" : "Capacity less than 400",
          r: "budget_per_student",
          symbol: "k_8",
          tip: {
          format: {
            school_name: true,
            building_condition: true,
            learning_environment: true,
            budget_per_student: true,
            r: false,
            y: false,
            x: false,
            symbol: false,
            fill: false
          }
          },
          channels: {
                    "School": "school_name",
                    "2023/24 Enrollment": "p223_total_count",
                    "Learning Environment": "learning_environment",
                    "Building Condition": "building_condition",
                    "School Capacity": "capacity",
                    "$/Student": "budget_per_student",
                    },}
        )]
                })
```

```js
Plot.plot({
  x: {label: "$/Student", tickPadding: 6, tickSize: 0, axis: "top",},
  y: {label: null, tickSize: 0},
  marginLeft: 100,
  marks: [
    Plot.ruleY(schools, {x: "budget_per_student", y: "school_name", stroke: "region", strokeWidth: 2}),
    Plot.dot(schools, {x: "budget_per_student", y: "school_name", fill: "region", r: 4, sort: {y: "-x"},})
  ]
})
```

On June 26th, 2024, the Seattle Public Schools provided an update on Well-Resourced
Schools to the Seattle Public School Board. In the meeting, SPS provided details
about the criteria that are considered when assessing school building resources.
SPS shared the presentation as well as an appendix with data on each elementary
school. Materials from the June 26th meeting can be found on the [SPS Website](https://www.seattleschools.org/news/safety-planning-update-and-progress-for-a-system-of-well-resourced-schools/).

The documents shared by SPS indicate the following criteria are used to assess a
"Well-Resourced School":

- Building condition
- Learning environment
- Capacity
- Location

To examine multiple criteria, this website aims to provide analysis of multiple dimensions
of data on Seattle public elementary schools. To start, the dashboard below shows
the data that SPS made available in the June 26th presentation's appendix. The following
three criteria are measured in the data.

- **Building Condition**: Each building is rated on a scale of 0 to 100: Excellent (100%), Good (90%), Fair (62%), Poor (30%), Unsatisfactory (0%). (Source: Säzän Environmental Services Facility Assessment Report, January 2022)
- **Learning Environment**: Ranges from 1 to 5; 1- Excellent, 2 - Good, 3 - Fair, 4 - Poor, 5 - Unsuitable
- **Capacity**: Number of students the building can accommodate for grades K-5 only for both elementary and K-8 schools

Additionally, the appendix included data on school-level administrative budgets.

As further analysis, I aim to include data and analysis that gives insights on the
fourth criteria, school location.

## Relationship Between Assessment Criteria

In the figure below, I have converted data on building condition, learning environment,
and building capacity by sorting the schools from 1 to 70. Where there are ties the
minimum value of ties is used.



## Data

For ease of viewing, the data provided by SPS are arranged in a single table below.

```js
function sparkbar(max) {
  return (x) => htl.html`<div style="
    background: var(--theme-green);
    color: black;
    font: 10px/1.6 var(--sans-serif);
    width: ${100 * x / max}%;
    float: right;
    padding-right: 3px;
    box-sizing: border-box;
    overflow: visible;
    display: flex;
    justify-content: end;">${x.toLocaleString("en-US")}`
}
```

```js
const schoolsRegion = view(
  Inputs.checkbox(
    d3.group(schools, (d) => d.middle_school_attendance_area),
    {label: "Middle School Attendance Areas",sort: "ascending", key: ["Aki Kurose", "Denny", "Eckstein", "Hamilton", "Jane Addams", "Madison", "McClure", "Meany", "Mercer", "Robert Eagle Staff", "Washington", "Whitman"]}
  )
);
```

```js
view(Inputs.table(schoolsRegion.flat(), {
  columns: [
    "school_name",
    "k_8",
    "middle_school_attendance_area",
    "building_condition",
    "learning_environment",
    "capacity",
    "p223_total_count",
    "total_budget",
    "budget_per_student",
  ],
  format: {
    "building_condition": sparkbar(d3.max(schools, d => d.building_condition)),
    "learning_environment": sparkbar(d3.max(schools, d => d.learning_environment)),
    "capacity": sparkbar(d3.max(schools, d => d.capacity)),
    "building_condition_rank": sparkbar(d3.max(schools, d => d.building_condition_rank)),
    "learning_environment_rank": sparkbar(d3.max(schools, d => d.learning_environment_rank)),
    "capacity_rank": sparkbar(d3.max(schools, d => d.capacity_rank)),
    "p223_total_count": sparkbar(d3.max(schools, d => d.p223_total_count)),
    "total_budget": sparkbar(d3.max(schools, d => d.budget)),
    "budget_per_student": sparkbar(d3.max(schools, d => d.budget_per_student))
  },
  header: {
    school_name: "School",
    k_8: "K-8",
    middle_school_attendance_area: "Middle School Area",
    building_condition: "Building Condition",
    learning_environment: "Learning Environment",
    capacity: "Building Capacity",
    p223_total_count: "Enrollment",
    total_budget: "Total Budget",
    budget_per_student: "Budget Per Student",
  }
}))
```

Data Sources:

- Seattle Public Schools, [June 26 School Board Meeting Update for Well-Resourced Schools](https://www.seattleschools.org/news/safety-planning-update-and-progress-for-a-system-of-well-resourced-schools/)
- Seattle Public Schools, [Enrollment Reporting P223](https://www.seattleschools.org/departments/dots/data-reporting/enrollment-reporting-p223/)
- King County, [GIS Open Data](https://gis-kingcounty.opendata.arcgis.com/)

---

If you have suggestions for modifications or improvements to this webpage, please
contact me @NKeleher (Twitter/X).

School location data (Latitude, Longitude, Zip Code) were sourced from the [King County Open GIS Portal](https://gis-kingcounty.opendata.arcgis.com/).

\* _Note: this site is not affiliated with SPS or with the Seattle School Board._
