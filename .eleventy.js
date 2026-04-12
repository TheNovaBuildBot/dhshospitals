module.exports = function(eleventyConfig) {
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy("src/_redirects");

  eleventyConfig.addCollection("posts", function(collectionApi) {
    return collectionApi.getFilteredByTag("post").sort((a, b) => b.date - a.date);
  });

  eleventyConfig.addFilter("dateFormat", function(date) {
    if (date === "now") date = new Date();
    return new Date(date).toLocaleDateString("en-IN", {
      year: "numeric", month: "long", day: "numeric"
    });
  });

  eleventyConfig.addFilter("dateToISO", function(date) {
    return new Date(date).toISOString();
  });

  eleventyConfig.addFilter("head", function(array, n) {
    if (!Array.isArray(array)) return array;
    return array.slice(0, n);
  });

  eleventyConfig.addFilter("truncate", function(str, len) {
    if (!str || str.length <= len) return str;
    return str.substring(0, len) + "...";
  });

  return {
    dir: { input: "src", output: "_site" },
    templateFormats: ["njk", "md"],
    markdownTemplateEngine: "njk"
  };
};
