import os
import time

from rich import inspect
import tqdm
from termcolor import cprint

from generate import generate

# Time alotted for each idea writing phase
BASIC_MELODIC_IDEA_MINUTES = 7
RHYTHM_SECTION_MINUTES = 9
FINAL_PRODUCTION = 7
# Number of SongSeeds to choose from
N_TO_CHOOSE_FROM = 4

# Generate and show seeds
print()
generated_seeds = [generate() for _ in range(N_TO_CHOOSE_FROM)]
for i, generation in enumerate(generated_seeds):
    inspect(generation, docs=False, title=f"Seed {i+1}", value=False)
# Choose a seed
chosen_seed_idx = int(input("\nPlease input your chosen seen number:")) - 1
chosen_seed = generated_seeds[chosen_seed_idx]
# Clear screen and show chosen seed
os.system("clear")
cprint("You've chosen:", "light_green")
inspect(chosen_seed, title=f"Chosen Seed", docs=False, value=False)
# Show tqdms timer for basic melodic idea
start = time.time()
cprint("Basic melodic idea:", "light_green")
for i in tqdm.tqdm(range(BASIC_MELODIC_IDEA_MINUTES * 60)):
    time.sleep(1)
cprint("Rhythm section:", "light_green")
# Show tqdms timer for rhythm section
for i in tqdm.tqdm(range(RHYTHM_SECTION_MINUTES * 60)):
    time.sleep(1)
cprint("Final production:", "light_green")
# Show tqdms timer for final production
for i in tqdm.tqdm(range(FINAL_PRODUCTION * 60)):
    time.sleep(1)
# Show final blinking message
print()
cprint(r"Finish and bounce!", "white", "on_light_red", attrs=["blink"])
input("")  # Wait for user to press enter (or any key)
end = time.time()
formatted_elapsed_time = time.strftime("%H:%M:%S", time.gmtime(end - start))
print(f"Total time elapsed: {formatted_elapsed_time}")
