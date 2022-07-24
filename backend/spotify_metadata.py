import json
import random
import itertools

class SpotifySongMetadata:
    def __init__(self) -> None:
        # dictionary for holding metadata parameters
        self.metadata = {}

        # seed parameters
        # these are required parameters for recommendations
        self.seed_attrs = [
            'seed_artists',
            'seed_genres',
            'seed_tracks',
        ]

        valid_fraction = lambda x: x >= 0.0 and x <= 1.0
        # prefixes for numerical parameters
        prefixes = [
            'target',
            'min',
            'max',
        ]
        # numerical parameter validators
        # dictionary, where key is name of the prefix-less attribute
        # and value is a function that validates the value of the attribute
        numerical_attr_validators = {
            'acousticness': valid_fraction,
            'danceability': valid_fraction,
            'energy': valid_fraction,
            'instrumentalness': valid_fraction,
            'liveness': valid_fraction,
            'loudness': lambda x: x <= 0,
            'mode': lambda x: x in (0, 1),
            'speechiness': valid_fraction,
            'valence': valid_fraction,
        }

        # add prefixes to all numerical attributes
        self.numerical_attrs = {
            f'{i[0]}_{i[1]}': numerical_attr_validators[i[1]]
            for i in itertools.product(prefixes, numerical_attr_validators)
        }

    def set(self, attr: str, value: any) -> None:
        """
        Set attribute value
        """
        if attr in self.seed_attrs:
            # seed attributes should be comma separated strings
            # this converts list of strings to comma separated string
            if not isinstance(value, str):
                value = ','.join(value)
        elif attr in self.numerical_attrs:
            if not self.numerical_attrs[attr](value):
                raise ValueError(
                    f'Invalid value {value} for attribute "{attr}"'
                )
        else:
            raise ValueError(f'Invalid attribute "{attr}"')

        self.metadata[attr] = value

    def set_from_dict(self, metadata_dict: dict) -> None:
        """
        Set attributes from dictionary.
        """
        for attr, value in metadata_dict.items():
            self.set(attr, value)

    # get value of attribute
    # returns None if attribute hasn't been set
    def get(self, attr: str) -> any:
        """
        Get value of attribute.
        Returns None if attribute hasn't been set.
        """

        if attr not in self.seed_attrs and attr not in self.numerical_attrs:
            raise ValueError(f'Invalid attribute "{attr}"')

        return self.metadata.get(attr)

    def randomize_seeds(self, limit=5) -> None:
        """
        Randomly sample from the seed values
        and get rid of the rest of them.
        This is for executing before getting a song recommendation.
        Spotify requires that there are at most 5 seed values.
        """

        for attr in self.seed_attrs:
            value = self.metadata.get(attr)

            if value is not None:
                # convert comma separated string to list fof strings
                value = value.strip().split(',')
                # choose a sample of seed values
                seed_subset = random.sample(value, min(limit, len(value)))
                # convert list of strings back to comma separated string
                value = ','.join(seed_subset)

                self.metadata[attr] = value

    # get metadata dictionary
    def dict(self) -> dict:
        return self.metadata

    # get metadata iterator for dictionary conversion
    def __iter__(self) -> any:
        for attr in self.metadata:
            yield (attr, self.metadata[attr])

    # convert and return metadata dictionary to string
    def __str__(self) -> str:
        return str(self.metadata)

    # convert and return metadata dictionary to pretty formatted string
    def __repr__(self) -> str:
        return json.dumps(self.metadata, sort_keys=True, indent=4)