# Limitations

## Known limitations

### 1. Heuristic scoring is not a learned classifier

The current detection engine does not train a supervised model on labeled data. It instead combines engineered linguistic features into a score. This makes the approach explainable and easy to debug, but it may miss subtle patterns that a trained model would learn.

### 2. Performance depends on dataset quality

Model quality depends heavily on how representative the human and AI examples are. If the dataset is small, noisy, or unbalanced, the evaluation metrics may be misleading.

### 3. Local perplexity is a proxy signal

The GPT-2 perplexity calculation is useful for identifying unusual word patterns, but it is not the same as determining whether a human or model generated text in a definitive way. Perplexity only captures one aspect of language behavior.

### 4. Sentence-level detection can be noisy

Some essays contain a mix of sentence types, structures, and styles. A single sentence may trigger a high AI-likelihood score even when the essay overall is human-written, or vice versa.

### 5. Risk of overfitting to style patterns

If the feature thresholds are tuned to one dataset, they may not generalize well across new essay prompts, educational contexts, or different writing styles.

### 6. Not suitable for high-stakes decisions without validation

This project is best viewed as a research and analysis tool rather than a final decision-making system for admissions or academic integrity reviews.

## Future improvements

### Model-based detection

The next major improvement is to train a supervised classifier using the prepared dataset. This could include:

- logistic regression
- random forest
- gradient boosting
- transformer-based classifiers
- lightweight embeddings or sentence-transformer models

### Better features

Additional features could include:

- semantic coherence metrics
- discourse markers and argument structure
- stance and hedging analysis
- syntactic parsing features
- stylometric profiling across the full essay

### Stronger evaluation workflow

Future enhancements could add:

- cross-validation
- ROC-AUC and PR-AUC metrics
- calibration curves
- per-class analysis and error reporting
- model artifact saving and experiment tracking

### UI improvements

The frontend could be extended with:

- score history
- sentence drill-down tools
- highlight toggles
- dataset evaluation dashboard
- a compare mode between essays

### Production readiness

For production deployment, the team would need:

- stronger privacy and data-handling controls
- secure model packaging and serving
- user-role management
- audit logging
- formal validation against institutional policies and legal review

## Summary

The system is already structured for explainable AI detection and evaluation. The main limitation is that it currently relies on heuristic signals rather than a trained discriminative model. The project is therefore best positioned as a strong research prototype with a clear path toward more robust data-driven classification.
