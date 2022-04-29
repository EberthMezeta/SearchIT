let doc = {
  results: {
    responseHeader: {
      status: 0,
      QTime: 7,
    },
    command: "build",
    suggest: {
      mySuggester: {
        pytho: {
          numFound: 1,
          suggestions: [
            {
              term: "python — Cómo obtener sinónimos de nltk WordNet Python",
              weight: 0,
              payload: "",
            },
          ],
        },
      },
    },
  },
};

console.log(doc)
