(() => {
  const loader = document.currentScript;
  const episode = /^\/tests\/video-delivery-(\d{4})(\d{2})(\d{2})\/(?:index\.html)?$/.exec(location.pathname);
  if (!episode) return;

  const client = document.createElement("script");
  client.src = "https://giscus.app/client.js";
  client.crossOrigin = "anonymous";
  client.async = true;
  Object.assign(client.dataset, {
    repo: "markjin-lab/markjin-lab.github.io",
    repoId: "R_kgDOVE_C8w",
    category: "Comments",
    categoryId: "DIC_kwDOVE_C884DHl3-",
    mapping: "specific",
    term: `认知输入讲解 · ${episode.slice(1).join("-")}`,
    strict: "1",
    reactionsEnabled: "1",
    inputPosition: "top",
    theme: "light",
    lang: "zh-CN",
    loading: "lazy",
  });
  loader.after(client);
})();
