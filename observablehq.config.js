// See https://observablehq.com/framework/config for documentation.
export default {
  // The project’s title; used in the sidebar and webpage titles.
  title: "Well-Resourced Schools",

  // The pages and sections in the sidebar. If you don’t specify this option,
  // all pages will be listed in alphabetical order. Listing pages explicitly
  // lets you organize them into sections and have unlisted pages.
  pages: [
    {
      name: "Data & Additional Analysis",
      pages: [
        {name: "By Region", path: "/school_regions"},
        {name: "Data Sources", path: "/data_sources"},
        // {name: "Building Metrics", path: "/building_rankings"}
      ]
    }
  ],

  // Some additional configuration options and their defaults:
  theme: ["glacier"], // try "light", "dark", "slate", etc.
  // header: "", // what to show in the header (HTML)
  // footer: "Built with Observable.", // what to show in the footer (HTML)
  toc: false, // whether to show the table of contents
  // pager: true, // whether to show previous & next links in the footer
  // sidebar: true // whether to show sidebar
  // root: "docs", // path to the source root for preview
  // output: "dist", // path to the output root for build
  // search: true, // activate search
};
