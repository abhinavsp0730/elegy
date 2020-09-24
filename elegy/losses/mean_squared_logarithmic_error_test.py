import elegy

from elegy.testing_utils import transform_and_run
import jax.numpy as jnp
import jax


# import debugpy

# print("Waiting for debugger...")
# debugpy.listen(5679)
# debugpy.wait_for_client()


@transform_and_run
def test_basic():

    y_true = jnp.array([[0.0, 1.0], [0.0, 0.0]])
    y_pred = jnp.array([[1.0, 1.0], [1.0, 0.0]])

    # Using 'auto'/'sum_over_batch_size' reduction type.
    msle = elegy.losses.MeanSquaredLogarithmicError()

    assert msle(y_true, y_pred) == 0.24022643

    # Calling with 'sample_weight'.
    assert msle(y_true, y_pred, sample_weight=jnp.array([0.7, 0.3])) == 0.12011322

    # Using 'sum' reduction type.
    msle = elegy.losses.MeanSquaredLogarithmicError(reduction=elegy.losses.Reduction.SUM)

    assert msle(y_true, y_pred) == 0.48045287

    # Using 'none' reduction type.
    msle = elegy.losses.MeanSquaredLogarithmicError(reduction=elegy.losses.Reduction.NONE)

    assert list(msle(y_true, y_pred)) == [0.24022643, 0.24022643]


@transform_and_run
def test_function():

    rng = jax.random.PRNGKey(42)

    y_true = jax.random.randint(rng, shape=(2, 3), minval=0, maxval=2)
    y_pred = jax.random.uniform(rng, shape=(2, 3))

    loss = elegy.losses.mean_squared_logarithmic_error(y_true, y_pred)

    assert loss.shape == (2,)
    
    first_log = jnp.log(jnp.maximum(y_true, utils.EPSILON) + 1.0)
    second_log = jnp.log(jnp.maximum(y_pred, utils.EPSILON) + 1.0)
    assert jnp.array_equal(loss, jnp.mean(jnp.square(first_log - second_log), axis=-1))


if __name__ == "__main__":

    test_basic()
    test_function()