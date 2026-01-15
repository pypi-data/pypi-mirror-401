# emic

**E**psilon **M**achine **I**nference & **C**haracterization

A Python framework for constructing and analyzing epsilon-machines based on computational mechanics.

> ⚠️ **This package is under active development.** The API is not yet stable.

## What is an Epsilon-Machine?

An epsilon-machine (ε-machine) is the minimal, optimal predictor of a stochastic process. It captures the intrinsic computational structure hidden in sequential data — the "causal states" that summarize all relevant history for predicting the future.

This framework implements algorithms for:
- Inferring ε-machines from observed sequences (CSSR and more)
- Computing complexity measures (statistical complexity, entropy rate, excess entropy)
- Visualizing and analyzing the discovered structure

## Installation

```bash
pip install emic
```

## Status

🚧 **Planning phase** — See the [GitHub repository](https://github.com/yourusername/emic) for development progress.

## Etymology

The name "emic" works on multiple levels:
- **Acronym**: **E**psilon **M**achine **I**nference & **C**haracterization
- **Linguistic**: In linguistics, "emic" refers to analysis *from within the system* — exactly what ε-machines reveal

## References

- Crutchfield, J.P. & Young, K. (1989). "Inferring Statistical Complexity"
- Shalizi, C.R. & Crutchfield, J.P. (2001). "Computational Mechanics: Pattern and Prediction, Structure and Simplicity"

## License

MIT
