"""Transfer Learning with MobileNetV2 on CIFAR-10."""

from typing import Any, Callable, Dict, List, Optional, Union

import numpy as np

from surfaces.modifiers import BaseModifier

from ..._base_transfer_learning import BaseTransferLearning


class MobileNetTransferLearningFunction(BaseTransferLearning):
    """Transfer Learning test function using pre-trained MobileNetV2.

    **What is optimized:**
    This function optimizes the transfer learning configuration when fine-tuning
    a pre-trained MobileNetV2 model (trained on ImageNet) for a new task (CIFAR-10).
    The search includes:
    - Freeze ratio (0.0-1.0): fraction of base model layers to freeze
    - Fine-tuning learning rate (1e-5, 1e-4, 1e-3)
    - Dropout rate for regularization (0.0, 0.3, 0.5)
    - Dense layer size before output (64, 128, 256)

    **Transfer learning concept:**
    Transfer learning leverages knowledge from a model pre-trained on a large dataset
    (ImageNet) and adapts it to a new task. Freezing early layers preserves low-level
    features (edges, textures) while allowing later layers to adapt to the new task.

    **What the score means:**
    The score is the validation accuracy (0.0 to 1.0) achieved after fine-tuning
    the pre-trained model on CIFAR-10. Higher scores indicate better transfer of
    knowledge from ImageNet to the new classification task.

    **Optimization goal:**
    MAXIMIZE the validation accuracy. The goal is to find the optimal balance between:
    - Freezing layers (preserving ImageNet features vs. task-specific adaptation)
    - Learning rate (fast convergence vs. catastrophic forgetting)
    - Regularization (preventing overfitting on small datasets)
    - Model capacity (dense layer size)

    **Computational cost:**
    Each evaluation involves fine-tuning a large pre-trained model, making this
    expensive. The default uses a subset of CIFAR-10 and few epochs to keep
    evaluation time reasonable (~40-80 seconds per evaluation on CPU).

    Parameters
    ----------
    n_epochs : int, default=5
        Number of fine-tuning epochs per evaluation.
    batch_size : int, default=32
        Training batch size.
    subset_size : int, default=3000
        Number of training samples to use (CIFAR-10 has 50000 total).
        Smaller values speed up training for prototyping.
    objective : str, default="maximize"
        Either "minimize" or "maximize".
    modifiers : list of BaseModifier, optional
        List of modifiers to apply to function evaluations.

    Examples
    --------
    >>> from surfaces.test_functions.machine_learning import MobileNetTransferLearningFunction
    >>> func = MobileNetTransferLearningFunction(n_epochs=3, subset_size=2000)
    >>> func.search_space
    {'freeze_ratio': [0.0, 0.5, 0.8, 1.0], 'learning_rate': [1e-05, 0.0001, 0.001], ...}
    >>> result = func({"freeze_ratio": 0.8, "learning_rate": 0.0001,
    ...                "dropout": 0.3, "dense_units": 128})
    >>> print(f"Validation accuracy: {result:.4f}")

    Notes
    -----
    Requires TensorFlow. Install with:
        pip install tensorflow

    The pre-trained MobileNetV2 model is downloaded automatically on first use.
    The function uses a subset of CIFAR-10 by default to keep evaluation time
    reasonable. For final benchmarking, increase subset_size and n_epochs.
    """

    name = "MobileNet Transfer Learning"
    _name_ = "mobilenet_transfer_learning"
    __name__ = "MobileNetTransferLearningFunction"

    para_names = ["freeze_ratio", "learning_rate", "dropout", "dense_units"]
    freeze_ratio_default = [0.0, 0.5, 0.8, 1.0]
    learning_rate_default = [1e-5, 1e-4, 1e-3]
    dropout_default = [0.0, 0.3, 0.5]
    dense_units_default = [64, 128, 256]

    def __init__(
        self,
        n_epochs: int = 5,
        batch_size: int = 32,
        subset_size: int = 3000,
        objective: str = "maximize",
        modifiers: Optional[List[BaseModifier]] = None,
        memory: bool = False,
        collect_data: bool = True,
        callbacks: Optional[Union[Callable, List[Callable]]] = None,
        catch_errors: Optional[Dict[type, float]] = None,
        use_surrogate: bool = False,
    ):
        self.n_epochs = n_epochs
        self.batch_size = batch_size
        self.subset_size = subset_size

        super().__init__(
            objective=objective,
            modifiers=modifiers,
            memory=memory,
            collect_data=collect_data,
            callbacks=callbacks,
            catch_errors=catch_errors,
            use_surrogate=use_surrogate,
        )

    @property
    def search_space(self) -> Dict[str, Any]:
        """Search space for transfer learning optimization."""
        return {
            "freeze_ratio": self.freeze_ratio_default,
            "learning_rate": self.learning_rate_default,
            "dropout": self.dropout_default,
            "dense_units": self.dense_units_default,
        }

    def _create_objective_function(self) -> None:
        """Create objective function for transfer learning."""
        import tensorflow as tf
        from tensorflow import keras
        from tensorflow.keras import layers
        from tensorflow.keras.applications import MobileNetV2

        # Load CIFAR-10 dataset
        (X_train, y_train), (X_val, y_val) = keras.datasets.cifar10.load_data()

        # Resize images to 96x96 (MobileNetV2 minimum input size)
        X_train_resized = tf.image.resize(X_train, (96, 96)).numpy()
        X_val_resized = tf.image.resize(X_val, (96, 96)).numpy()

        # Preprocess for MobileNetV2 (scale to [-1, 1])
        X_train_preprocessed = keras.applications.mobilenet_v2.preprocess_input(
            X_train_resized
        )
        X_val_preprocessed = keras.applications.mobilenet_v2.preprocess_input(
            X_val_resized
        )

        # Use subset for faster evaluation
        if self.subset_size < len(X_train_preprocessed):
            indices = np.random.RandomState(42).choice(
                len(X_train_preprocessed), self.subset_size, replace=False
            )
            X_train_preprocessed = X_train_preprocessed[indices]
            y_train = y_train[indices]

        # Take smaller validation set too
        val_size = min(1000, len(X_val_preprocessed))
        X_val_preprocessed = X_val_preprocessed[:val_size]
        y_val = y_val[:val_size]

        n_epochs = self.n_epochs
        batch_size = self.batch_size

        def objective_function(params: Dict[str, Any]) -> float:
            # Load pre-trained MobileNetV2 (without top layers)
            base_model = MobileNetV2(
                input_shape=(96, 96, 3), include_top=False, weights="imagenet"
            )

            # Freeze layers based on freeze_ratio
            freeze_ratio = params["freeze_ratio"]
            n_layers = len(base_model.layers)
            n_freeze = int(n_layers * freeze_ratio)

            for layer in base_model.layers[:n_freeze]:
                layer.trainable = False
            for layer in base_model.layers[n_freeze:]:
                layer.trainable = True

            # Build model
            model = keras.Sequential([
                base_model,
                layers.GlobalAveragePooling2D(),
                layers.Dropout(params["dropout"]),
                layers.Dense(params["dense_units"], activation="relu"),
                layers.Dense(10, activation="softmax"),
            ])

            # Compile model
            model.compile(
                optimizer=keras.optimizers.Adam(learning_rate=params["learning_rate"]),
                loss="sparse_categorical_crossentropy",
                metrics=["accuracy"],
            )

            # Train model (suppress output)
            history = model.fit(
                X_train_preprocessed,
                y_train,
                batch_size=batch_size,
                epochs=n_epochs,
                validation_data=(X_val_preprocessed, y_val),
                verbose=0,
            )

            # Return final validation accuracy
            val_accuracy = history.history["val_accuracy"][-1]
            return val_accuracy

        self.pure_objective_function = objective_function
