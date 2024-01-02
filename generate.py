import random

import descriptors
from schema import Swing, Tempo, SongSeed
from lyric_ideas import INTERESTING_LYRICAL_IDEAS


SWING_PROB = 0.2
WEIGHT_SMOOTHING_CONSTANT = 0.01
TEMPO_RANGE_WEIGHTS_BY_SWING = {
    Swing.TRUE: {
        Tempo.EIGHTYISH: 0.025,
        Tempo.NINETYISH: 0.05,
        Tempo.HUNDREDISH: 0.225,
        Tempo.HUNDREDTENISH: 0.225,
        Tempo.HUNDREDTWENTYISH: 0.225,
        Tempo.HUNDREDTHIRTYISH: 0.1,
        Tempo.HUNDREDFOURTYISH: 0.075,
        Tempo.HUNDREDFIFTYISH: 0.025,
        Tempo.HUNDREDSIXTYISH: 0.025,
        Tempo.HUNDREDSEVENTYISH: 0.025,
    },
    Swing.FALSE: {
        Tempo.EIGHTYISH: 0.025,
        Tempo.NINETYISH: 0.075,
        Tempo.HUNDREDISH: 0.225,
        Tempo.HUNDREDTENISH: 0.275,
        Tempo.HUNDREDTWENTYISH: 0.225,
        Tempo.HUNDREDTHIRTYISH: 0.075,
        Tempo.HUNDREDFOURTYISH: 0.025,
        Tempo.HUNDREDFIFTYISH: 0.025,
        Tempo.HUNDREDSIXTYISH: 0.025,
        Tempo.HUNDREDSEVENTYISH: 0.025,
    },
}


def get_descriptor_probability_given_tempo_and_swing(
    descriptor: descriptors.Descriptor, tempo_range: Tempo, swing: Swing
):
    # Get P(tempo | descriptor)
    p_dist_of_temp_given_descr = descriptor.tempo_prob_dist
    if p_dist_of_temp_given_descr is None:
        return len(tempo_range.value) / (175 - 76)
    tempo_min_bound, tempo_upper_bound = tempo_range.value[0], tempo_range.value[-1]
    p_tempo_within_range_given_descr = p_dist_of_temp_given_descr.cdf(
        tempo_upper_bound
    ) - p_dist_of_temp_given_descr.cdf(tempo_min_bound)
    # Get P(swing | descriptor)
    p_swing_given_descr = descriptor.swing_prob
    # P(word | tempo & swing) = product of these (independent) events
    return p_tempo_within_range_given_descr * p_swing_given_descr


def generate() -> SongSeed:
    """Generates and returns a SongSeed."""
    # Generate swing
    swing = random.choices(
        [Swing.TRUE, Swing.FALSE], weights=[SWING_PROB, 1 - SWING_PROB]
    )[0]
    # Select tempo given swing
    tempo_ranges = list(TEMPO_RANGE_WEIGHTS_BY_SWING[swing].keys())
    tempo_range_selection_weights = list(TEMPO_RANGE_WEIGHTS_BY_SWING[swing].values())
    tempo_range = random.choices(tempo_ranges, weights=tempo_range_selection_weights)[0]
    # Select a single-word descriptor
    weights = []
    for descriptor in descriptors.SINGLE_WORD:
        weight = get_descriptor_probability_given_tempo_and_swing(
            descriptor, tempo_range, swing
        )
        weights.append(weight * descriptor.affinity + WEIGHT_SMOOTHING_CONSTANT)
    single_word_descriptor = random.choices(descriptors.SINGLE_WORD, weights=weights)[0]
    # Select a review descriptor
    weights = []
    for descriptor in descriptors.FROM_REVIEWS:
        weight = get_descriptor_probability_given_tempo_and_swing(
            descriptor, tempo_range, swing
        )
        weights.append(weight * descriptor.affinity + WEIGHT_SMOOTHING_CONSTANT)
    review_descriptor = random.choices(descriptors.FROM_REVIEWS, weights=weights)[0]
    # Select a lyric prompt
    lyric_prompt = random.choice(INTERESTING_LYRICAL_IDEAS)
    # Return SongSeed
    return SongSeed(
        swing=str(swing),
        tempo=f"{tempo_range.value[0]}-{tempo_range.value[-1]}",
        attitude=single_word_descriptor.text,
        sensation=review_descriptor.text,
        lyric_prompt=lyric_prompt,
    )
