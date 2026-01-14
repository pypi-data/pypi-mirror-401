import os
import warnings

import h5py
import numpy as np

from .utils import gen_credible_interval


PARENT_FIELD = dict(
    hyperparameter_descriptions='hyperparameters',
    hyperparameter_units='hyperparameters',
    hyperparameter_latex_labels='hyperparameters',
    event_waveforms='events',
    event_sample_IDs='events',
    event_parameter_units='event_parameters',
)


class PopulationResult:
    """
    Class for storing and retrieving population-level data products for gravitational-wave
    analyses.
    """
    def __init__(
            self, fname=None, hyperparameters=None, hyperparameter_descriptions=None,
            hyperparameter_units=None, hyperparameter_latex_labels=None,  references=None,
            model_names=None, events=None, event_waveforms=None, event_sample_IDs=None,
            event_parameters=None, event_parameter_units=None, verbose=True,
            default_h5py_kwargs={}):
        """
        Parameters
        ----------
        fname: str
            Name of h5 file.
        hyperparameters: list
            List of hyperparameter names.
        hyperparameter_descriptions: list
            List of descriptions for `hyperparameters`.
        hyperparameter_units: list
            List of units for `hyperparameters`. For compatibility with the hdf5 format, each entry
            must be a str, however it is recommended that these entries are valid arguments for
            astropy.units.Unit.
        hyperparameter_latex_labels: list
            List of latex labels for `hyperparameters`.
        references: list
            List of references for analyses, data products and models.
        model_names: list
            List of population models used.
        events: list
            List of events used in analyses.
        event_waveforms: list or str
            List of waveforms in corresponding order to `events` or a single string denoting the
            waveform used for all events.
        event_sample_IDs: list, int, or str
            List of IDs for PE sample versions in corresponding order to `events` or a single
            string/int denoting the version used for all events.
        event_parameters: list
            List of event-level parameter names (e.g. m1, m2, chi_eff) in corresponding order to
            `reweighted_event_samples`, `rewighted_injections` and/or `fair_population_draws`.
        event_parameter_units: list
            List of units for `event_parameters`. For compatibility with the hdf5 format, each
            entry must be a str, however it is recommended that these entries are valid arguments
            for astropy.units.Unit.
        verbose: bool
            Whether to print information on popsummary file.
        default_h5py_kwargs: dict
            Default kwargs to be passed when storing data to popsummary file with
            h5py.File.create_dataset.
        """
        if not isinstance(fname, str):
            raise ValueError("filename (fname) must be given and must be a string")
        self.fname = fname

        self.default_h5py_kwargs = default_h5py_kwargs

        if not os.path.exists(fname):
            if verbose:
                print(f"creating a new popsummary file: {self.fname}")
            with h5py.File(fname, 'w') as f:
                f.create_group('posterior')
                f.create_group('prior')
                self.set_metadata('hyperparameters', hyperparameters)
                self.set_metadata('hyperparameter_descriptions', hyperparameter_descriptions)
                self.set_metadata('hyperparameter_units', hyperparameter_units)
                self.set_metadata('hyperparameter_latex_labels', hyperparameter_latex_labels)
                self.set_metadata('references', references)
                self.set_metadata('model_names', model_names)
                self.set_metadata('events', events)
                self.set_metadata('event_waveforms', event_waveforms)
                self.set_metadata('event_sample_IDs', event_sample_IDs)
                self.set_metadata('event_parameters', event_parameters)
                self.set_metadata('event_parameter_units', event_parameter_units)
        else:
            if verbose:
                print(f"opening existing popsummary file: {self.fname}")
        

    def get_metadata(self, field=None):
        """
        Retrieves metadata from popsummary file.
        
        Parameters
        ----------
        field: str
            Type of metadata to retrieve (e.g. 'events', 'model_names', etc.) if `None`, returns
            dictionary of all entries.

        Returns
        -------
        metadata: list or str
            Requested metadata.
        """
        with h5py.File(self.fname, 'r') as f:

            if field is None:
                return {_field: f.attrs[_field]
                        for _field in f.attrs.keys()}
            elif field in f.attrs.keys():
                return f.attrs[field]
            else:
                warnings.warn(f"metadata '{field}' does not exist")
    

    def set_metadata(self, field, metadata, overwrite=False):
        """
        Saves metadata to popsummary file.
        
        Parameters
        ----------
        field: str
            Type of metadata to save (e.g. 'events', 'model_names', etc.).
        metadata: str
            Contents to save to field.
        overwrite: bool
            Whether to overwrite existing metadata.
        """
        with h5py.File(self.fname, 'a') as f:

            self._try_overwrite(f.attrs, field, overwrite)
                
            if metadata is not None:

                if field in PARENT_FIELD.keys():
                    if PARENT_FIELD[field] not in f.attrs.keys():
                        raise Exception(
                            f"`{PARENT_FIELD[field]}` must be assigned before `{field}`")
                    if (isinstance(metadata, list) and
                        len(metadata) != len(f.attrs[PARENT_FIELD[field]])):
                        raise Exception(
                            f"length of `{field}` ({len(metadata)}) must match length of "
                            f"`{PARENT_FIELD[field]}` ({len(f.attrs[PARENT_FIELD[field]])})")

                f.attrs[field] = metadata


    def get_metadata_keys(self, verbose=True):
        """
        Returns the keys for all stored metadata items.

        Parameters
        ----------
        verbose: bool
            Whether to print dialogue listing the available keys.
        
        Returns
        -------
        keys: list
            List of keys for stored metadata entries.
        """
        with h5py.File(self.fname, 'r') as f:

            keys = list(f.attrs.keys())

            if verbose:
                print(f"keys for stored metadata are: {keys}")
            return keys


    def get_hyperparameter_samples(
            self, hyper_sample_idx=None, hyperparameters=None, group='posterior'):
        """
        Retrieves hyperparameter samples from popsummary file.
        
        Parameters
        ----------
        hyper_sample_idx: int or slice
            Hyper samples to retrieve (`None` gives all hyper samples).
        hyperparameters: str or list of str
            Name(s) of hyper-parameters to retrieve (`None` gives all parameters).
        group: str
            Group to retrieve samples from ('posterior' or 'prior').

        Returns
        -------
        hyperparameter_samples: 2D array
            numpy array of data with shape `(NumberOfHyperSamples,NumberOfPopulationDimensions)`.
        """
        with h5py.File(self.fname, 'r') as f:

            mask_hyper_sample = self._mask_with_idx(hyper_sample_idx)
            mask_hyperparameter = self._mask_with_metadata(f, 'hyperparameters', hyperparameters)
            
            return np.array(f[group]['hyperparameter_samples']
            )[mask_hyper_sample,:][:,mask_hyperparameter]


    def set_hyperparameter_samples(
            self, hyperparameter_samples, overwrite=False, group='posterior', h5py_kwargs={}):
        """
        Saves hyperparameter samples to popsummary file.
        
        Parameters
        ----------
        hyperparameter_samples: 2D array
            numpy array of data with shape (NumberOfHyperSamples,NumberOfPopulationDimensions).
        overwrite: bool
            Whether to overwrite existing dataset.
        group: str
            Group to save samples to ('posterior' or 'prior').
        h5py_kwargs: dict
            Keyword arguments passed to h5py.File.create_dataset, overwrites arguments in
            self.default_h5py_kwargs.
        """
        _h5py_kwargs = dict(self.default_h5py_kwargs, **h5py_kwargs)

        hyperparameter_samples = np.asarray(hyperparameter_samples)
        
        with h5py.File(self.fname, 'a') as f:

            self._verify_input(
                f, 'hyperparameter_samples', hyperparameter_samples, required_size=2,
                parent_key='hyperparameters', parent_axis=1)
            self._try_overwrite(f[group], 'hyperparameter_samples', overwrite)
                
            f[group].create_dataset(
                'hyperparameter_samples', data=hyperparameter_samples, **_h5py_kwargs)
        

    def get_reweighted_event_samples(
            self, events=None, draw_idx=None, hyper_sample_idx=None,
            use_hyperparameter_sample_idx_map=False, parameters=None, group="posterior"):
        """
        Retrieves reweighted event samples from popsummary file.

        Reweighted event samples are posterior samples for each GW event's properties (such as
        mass_1, a_1, redshift, etc.), but reweighted to the population described in the popsummary
        file.
        
        Parameters
        ----------
        events: str or list of str
            Names of events to retrieve samples from (`None` gives all events).
        draw_idx: int or slice
            Draws to retrieve (`None` gives all draws).
        hyper_sample_idx: int or slice
            Hyper samples to retrieve event samples for (`None` gives all hyper samples).
        use_hyperparameter_sample_idx_map: bool, default False
            If `True` and the `hyperparameter_sample_idx_map` attribute is not `None`, the
            `hyper_sample_idx` array specified will refer to indices of the
            `hyperparameter_samples`. If `False`, `hyper_sample_idx` will refer to the indices of
            the array stored in the `reweighted_injections` data set along its third
            (`NumberOfHypersamples`) dimension. 
        parameters: str or list of str
            Parameters to retrieve event samples for (`None` gives all parameters).
        group: str
            Group to retrieve samples from ('posterior' or 'prior').

        Returns
        -------
        reweighted_event_samples: 4D array
            numpy array of data with shape
            `(NumberOfEvents,NumberOfDraws,NumberOfHyperSamples,NumberOfEventDimensions)`.
        """
        with h5py.File(self.fname, 'r') as f:
            
            mask_event = self._mask_with_metadata(f, 'events', events)
            mask_draw = self._mask_with_idx(draw_idx)
            if use_hyperparameter_sample_idx_map:
                self._check_for_hyperparameter_sample_idx_map(f[group]['reweighted_event_samples'])
                mask_hyper_sample = self._mask_with_metadata(
                    f[group]['reweighted_event_samples'], 'hyperparameter_sample_idx_map',
                    hyper_sample_idx)
            else:
                mask_hyper_sample = self._mask_with_idx(hyper_sample_idx)
            mask_parameter = self._mask_with_metadata(f, 'event_parameters', parameters)

            return np.array(f[group]['reweighted_event_samples']
            )[mask_event,:,:,:][:,mask_draw,:,:][:,:,mask_hyper_sample,:][:,:,:,mask_parameter]
        

    def set_reweighted_event_samples(
            self, reweighted_event_samples, hyperparameter_sample_idx_map=None, overwrite=False,
            group='posterior', h5py_kwargs={}):
        """
        Saves reweighted event samples to popsummary file.

        Reweighted event samples are posterior samples for each GW event's properties (such as
        mass_1, a_1, redshift, etc.), but reweighted to the population described in the popsummary
        file.

        Parameters
        ----------
        reweighted_event_samples: 4D array
            numpy array of data with shape
            (NumberOfEvents,NumberOfDraws,NumberOfHyperSamples,NumberOfEventDimensions).
        hyperparameter_sample_idx_map: array, optional
            Array of indices that map to the corresponding hyperprior/posterior samples. Should be
            used when reweighted_event_samples are calculated for only a subset of the
            hyperprior/posterior samples. `hypersample_idx_map` should hold the indices for that
            subset from `hyperparameter_samples`. Default `None`.
        overwrite: bool
            Whether to overwrite existing dataset.
        group: str
            Group to save samples to ('posterior' or 'prior').
        h5py_kwargs: dict
            Keyword arguments passed to h5py.File.create_dataset, overwrites arguments in
            self.default_h5py_kwargs.
        """
        _h5py_kwargs = dict(self.default_h5py_kwargs, **h5py_kwargs)

        reweighted_event_samples = np.asarray(reweighted_event_samples)     

        with h5py.File(self.fname, 'a') as f:

            self._verify_input(
                f, 'reweighted_event_samples', reweighted_event_samples, required_size=4,
                parent_key='events', parent_axis=0)           
            self._try_overwrite(f[group], 'reweighted_event_samples', overwrite)

            f[group].create_dataset(
                'reweighted_event_samples', data=reweighted_event_samples, **_h5py_kwargs)
            self._set_hyperparameter_sample_idx_map(
                f[group]['reweighted_event_samples'], hyperparameter_sample_idx_map)


    def get_reweighted_injections(
            self, events_idx=None, catalog_idx=None, hyper_sample_idx=None,
            use_hyperparameter_sample_idx_map=False, parameters=None, group="posterior"):
        """
        Retrieves reweighted injections from popsummary file.

        Reweighted injections are samples of detections found through mock injections in GW search
        pipelines (from some reference distribution), reweighted to the population in the
        popsummary file.  
        
        Parameters
        ----------
        events_idx: int or slice
            Indices of simulated events in each "catalog" of simulated events from injections. Each
            catalog has some number of reweighted injections, and these indices correspond to the
            indices of those reweighted injections that the user wants returned. `None` gives all
            events.
        catalog_idx: int or slice
            Catalogs to retrieve (`None` gives all catalogs).
        hyper_sample_idx: int or slice
            Hyper samples to retrieve injections for (`None` gives all hyper samples).
        use_hyperparameter_sample_idx_map: bool, default False
            If `True` and the `hyperparameter_sample_idx_map` attribute is not `None`, the
            `hyper_sample_idx` array specified will refer to indices of the
            `hyperparameter_samples`. If `False`, `hyper_sample_idx` will refer to the indices of
            the array stored in the `reweighted_injections` data set along its third
            (`NumberOfHypersamples`) dimension. 
        parameters: str or list of str
            Parameters to retrieve event samples for (`None` gives all parameters).
        group: str
            Group to retrieve injections from ('posterior' or 'prior').

        Returns
        -------
        reweighted_injections: 4D array
            numpy array of data with shape
            `(NumberOfEvents,NumberOfCatalogs,NumberOfHyperSamples,NumberOfInjectionDimensions)`.
        """
        with h5py.File(self.fname, 'r') as f:

            mask_event = self._mask_with_idx(events_idx)
            mask_catalog = self._mask_with_idx(catalog_idx)
            if use_hyperparameter_sample_idx_map:
                self._check_for_hyperparameter_sample_idx_map(f[group]['reweighted_injections'])
                mask_hyper_sample = self._mask_with_metadata(
                    f[group]['reweighted_injections'], 'hyperparameter_sample_idx_map',
                    hyper_sample_idx)
            else:
                mask_hyper_sample = self._mask_with_idx(hyper_sample_idx)
            mask_parameter = self._mask_with_metadata(f, 'event_parameters', parameters)
                
            return np.array(f[group]['reweighted_injections']
            )[mask_event,:,:,:][:,mask_catalog,:,:][:,:,mask_hyper_sample,:][:,:,:,mask_parameter]     
     

    def set_reweighted_injections(
            self, reweighted_injections, hyperparameter_sample_idx_map=None, overwrite=False,
            group="posterior", h5py_kwargs={}):
        """
        Saves reweighted injections to popsummary file.
       
        Reweighted injections are samples of detections found through mock injections in GW search
        pipelines (from some reference distribution), reweighted to the population in the
        popsummary file. 

        Parameters
        ----------
        reweighted_injections: 4D array
            numpy array of data with shape
            (NumberOfEvents,NumberOfCatalogs,NumberOfHyperSamples,NumberOfInjectionDimensions).
        hyperparameter_sample_idx_map: array, optional
            Array of indices that map to the corresponding hyperprior/posterior samples. Should be
            used when reweighted_event_samples are calculated for only a subset of the
            hyperprior/posterior samples. `hypersample_idx_map` should hold the indices for that
            subset from `hyperparameter_samples`. Defaults to `None`.
        overwrite: bool
            Whether to overwrite existing dataset.
        group: str
            Group to save injections to ('posterior' or 'prior').
        h5py_kwargs: dict
            Keyword arguments passed to h5py.File.create_dataset, overwrites arguments in
            self.default_h5py_kwargs.
        """
        _h5py_kwargs = dict(self.default_h5py_kwargs, **h5py_kwargs)

        reweighted_injections = np.asarray(reweighted_injections)

        with h5py.File(self.fname, 'a') as f:

            self._verify_input(f, 'reweighted_injections', reweighted_injections, required_size=4)
            self._try_overwrite(f[group], 'reweighted_injections', overwrite)

            f[group].create_dataset(
                'reweighted_injections', data=reweighted_injections, **_h5py_kwargs)
            self._set_hyperparameter_sample_idx_map(
                f[group]['reweighted_injections'], hyperparameter_sample_idx_map)

            
    def get_fair_population_draws(
            self, draw_idx=None, hyper_sample_idx=None, use_hyperparameter_sample_idx_map=False,
            parameters=None, group="posterior"):
        """
        Retrieves fair population draws from popsummary file.
        
        Parameters
        ----------
        draw_idx: int or slice
            Draws to retrieve (`None` gives all draws).
        hyper_sample_idx: int or slice
            Hyper samples to retrieve draws for (`None` gives all hyper samples).
        use_hyperparameter_sample_idx_map: bool, default False
            If `True` and the `hyperparameter_sample_idx_map` attribute is not `None`, the
            `hyper_sample_idx` array specified will refer to indices of the
            `hyperparameter_samples`. If `False`, `hyper_sample_idx` will refer to the indices of
            the array stored in the `reweighted_injections` data set along its third
            (`NumberOfHypersamples`) dimension. 
        parameters: str or list of str
            Parameters to retrieve event samples for (`None` gives all parameters).
        group: str
            Group to retrieve injections from ('posterior' or 'prior').

        Returns
        -------
        fair_population_draws: 3D array
            numpy array of data with shape
            `(NumberOfDraws NumberOfHyperSamples,NumberOfEventDimensions)`.
        """
        with h5py.File(self.fname, 'r') as f:     
                
            mask_draw = self._mask_with_idx(draw_idx)
            if use_hyperparameter_sample_idx_map:
                self._check_for_hyperparameter_sample_idx_map(f[group]['fair_population_draws'])
                mask_hyper_sample = self._mask_with_metadata(
                    f[group]['fair_population_draws'], 'hyperparameter_sample_idx_map',
                    hyper_sample_idx)
            else:
                mask_hyper_sample = self._mask_with_idx(hyper_sample_idx)
            mask_parameter = self._mask_with_metadata(f, 'event_parameters', parameters)
                
            return np.array(f[group]['fair_population_draws']
            )[mask_draw,:,:][:,mask_hyper_sample,:][:,:,mask_parameter] 

        
    def set_fair_population_draws(
            self, fair_population_draws, hyperparameter_sample_idx_map=None, overwrite=False,
            group="posterior", h5py_kwargs={}):
        """
        Saves fair population draws to popsummary file.
        
        Parameters
        ----------
        fair_population_draws: 3D array
            numpy array of data with shape
            (NumberOfDraws,NumberOfHyperSamples,NumberOfEventDimensions).
        hyperparameter_sample_idx_map: array, optional
            Array of indices that map to the corresponding hyperprior/posterior samples. Should be
            used when reweighted_event_samples are calculated for only a subset of the
            hyperprior/posterior samples. `hypersample_idx_map` should hold the indices for that
            subset from `hyperparameter_samples`. Default `None`.
        overwrite: bool
            Whether to overwrite existing dataset.
        group: str
            Group to save draws to ('posterior' or 'prior').
        h5py_kwargs: dict
            Keyword arguments passed to h5py.File.create_dataset, overwrites arguments in
            self.default_h5py_kwargs.
        """
        _h5py_kwargs = dict(self.default_h5py_kwargs, **h5py_kwargs)

        fair_population_draws = np.asarray(fair_population_draws)
        
        with h5py.File(self.fname, 'a') as f:

            self._verify_input(f, 'fair_population_draws', fair_population_draws, required_size=3)
            self._try_overwrite(f[group], 'fair_population_draws', overwrite)
            
            f[group].create_dataset(
                'fair_population_draws', data=fair_population_draws, **_h5py_kwargs)
            self._set_hyperparameter_sample_idx_map(
                f[group]['fair_population_draws'], hyperparameter_sample_idx_map)
            

    def get_rates_on_grids(
            self, grid_key, hyper_sample_idx=None, use_hyperparameter_sample_idx_map=False,
            return_params=False, return_attributes=None, group="posterior"):
        """
        Retrieves rates on grids from popsummary file.
        
        Parameters
        ----------
        grid_key: str
            Key for rates dataset (e.g. 'primary_mass').
        hyper_sample_idx: int or slice
            Hyper samples to retrieve rates for (`None` gives all hyper samples).
        use_hyperparameter_sample_idx_map: bool, default False
            If `True` and the `hyperparameter_sample_idx_map` attribute is not `None`, the
            `hyper_sample_idx` array specified will refer to indices of the
            `hyperparameter_samples`. If `False`, `hyper_sample_idx` will refer to the indices of
            the array stored in the data set along its (`NumberOfHypersamples`) dimension. 
        return_params: bool
            Whether to return parameter labels for grid.
        return_attributes: bool, str or list
            Optional additional attributes to return as `dict` if `True`, returns all attributes
            (returns after params if return_params=`True`).
        group: str
            Group to retrieve injections from ('posterior' or 'prior').
        
        Returns
        -------
        positions: 2D array
            numpy array of grid positions at which rates are calculated with shape
            `(NumberOfParameters,NumberOfGridPoints)`.
        rates: 2D array
            numpy array of rates calculated on grid with shape
            `(NumberOfHypersamples,NumberOfGridPoints)`. This represents either the rate or PDF at
            a given grid point for a given hypersample.
        grid_params: str or list
            List of parameter names for which rates are calculated, returned if `return_params=True`.
        attributes: string or list
            List of optional additional attributes, returned if `return_attributes` specified.
        """
        with h5py.File(self.fname, 'r') as f:
            
            if use_hyperparameter_sample_idx_map:
                self._check_for_hyperparameter_sample_idx_map(
                    f[group]['rates_on_grids'][grid_key])
                mask_hyper_sample = self._mask_with_metadata(
                    f[group]['rates_on_grids'][grid_key], 'hyperparameter_sample_idx_map', 
                    hyper_sample_idx)
            else:
                mask_hyper_sample = self._mask_with_idx(selections=hyper_sample_idx)

            ret = (
                np.array(f[group]['rates_on_grids'][grid_key]['positions']),
                np.array(f[group]['rates_on_grids'][grid_key]['rates'])[mask_hyper_sample, ...],)
            
            if return_params:
                ret += (f[group]['rates_on_grids'][grid_key].attrs['parameters'],)

            if return_attributes is not None:
                ret_attrs = dict()
                if return_attributes == True:
                    for attribute in f[group]['rates_on_grids'][grid_key].attrs:
                        ret_attrs[attribute] = (
                            f[group]['rates_on_grids'][grid_key].attrs[attribute])
                elif isinstance(return_attributes, list):
                    for attribute in return_attributes:
                        ret_attrs[attribute] = (
                            f[group]['rates_on_grids'][grid_key].attrs[attribute])
                else:
                    ret_attrs[return_attributes] = (
                        f[group]['rates_on_grids'][grid_key].attrs[return_attributes])
                ret += (ret_attrs,)

            return ret
        

    def set_rates_on_grids(
            self, grid_key, grid_params, positions, rates, hyperparameter_sample_idx_map=None,
            attribute_keys=None, attributes=None, overwrite=False, group="posterior",
            h5py_kwargs={}):
        """
        Saves rates on grids to popsummary file.
        
        Parameters
        ----------
        grid_key: str
            Key for rates dataset (e.g. 'primary_mass').
        grid_params: str or list
            List of parameter names for which rates are calculated.
        positions: 2D array
            numpy array of grid positions at which rates are calculated with shape
            `(NumberOfParameters,NumberOfGridPoints)`. The grid positions need not be a rectangular
            grid. Each `NumberOfParameters`-dimensional point at which the rate/PDF is evaluated is
            written out. There are `NumberOfGridPoints` points at which the rate/PDF is evaluated.
        rates: 2D array
            numpy array of rates calculated on grid with shape
            `(NumberOfHypersamples,NumberOfGridPoints)`. This represents either the rate or pdf at
            a given grid point for a given hypersample.
        hyperparameter_sample_idx_map: array, optional
            Array of indices that map to the corresponding hyperprior/posterior samples. Should be
            used when data set corresponds to a subset of the hyperprior/posterior samples.
            `hyperparameter_sample_idx_map` should hold the indices for that subset from
            `hyperparameter_samples`. Default `None`.
        attribute_keys: string or list
            List of keys for optional additional attributes (must match length of attributes).
        attributes: string or list
            List of optional additional attributes (must match length of attribute_keys).
        overwrite: bool
            Whether to overwrite existing dataset.
        group: str
            Group to save draws to ('posterior' or 'prior').
        h5py_kwargs: dict
            Keyword arguments passed to h5py.File.create_dataset, overwrites arguments in
            self.default_h5py_kwargs.
        """
        _h5py_kwargs = dict(self.default_h5py_kwargs, **h5py_kwargs)

        positions = np.atleast_2d(positions)
        rates = np.asarray(rates)

        if isinstance(grid_params, str):
            grid_params = [grid_params]
        if len(grid_params) != positions.shape[0]:
            raise Exception(
                f"length of `grid_params` ({len(grid_params)}) should match length of axis 0 of "
                f"`positions` ({positions.shape[0]})")

        with h5py.File(self.fname, 'a') as f:

            if 'rates_on_grids' not in list(f[group].keys()):
                f[group].create_group('rates_on_grids')

            self._verify_input(f, 'positions', positions, required_size=2)
            self._verify_input(f, 'rates', rates, required_size=2)  
            self._try_overwrite(f[group]['rates_on_grids'], grid_key, overwrite)
                
            f[group]['rates_on_grids'].create_group(grid_key)
            f[group]['rates_on_grids'][grid_key].attrs['parameters'] = grid_params
            f[group]['rates_on_grids'][grid_key].create_dataset(
                'positions', data=positions, **_h5py_kwargs)
            f[group]['rates_on_grids'][grid_key].create_dataset(
                'rates', data=rates, **_h5py_kwargs)
            
            self._set_hyperparameter_sample_idx_map(
                f[group]['rates_on_grids'][grid_key], hyperparameter_sample_idx_map)

            if attributes is not None:
                if attribute_keys is None:
                    raise Exception("setting `attributes` requires `attribute_keys`")
                if isinstance(attribute_keys, (list, np.ndarray)):
                    for attr_idx in range(len(attributes)):
                        f[group]['rates_on_grids'][grid_key].attrs[attribute_keys[attr_idx]] = (
                            attributes[attr_idx])
                else:
                    f[group]['rates_on_grids'][grid_key].attrs[attribute_keys] = attributes
    

    def get_rates_on_grids_keys(self, verbose=True, group="posterior"):
        """
        Returns the keys for all items stored using `set_rates_on_grids`.

        Parameters
        ----------
        verbose: bool
            Whether to print dialogue listing the available keys.
        group: str
            Group to retrieve keys for ('posterior' or 'prior').
        
        Returns
        -------
        keys: list
            List of keys for stored rates.
        """
        with h5py.File(self.fname, 'r') as f:

            if 'rates_on_grids' not in f[group].keys():
                keys = None
            else:
                keys = list(f[group]['rates_on_grids'].keys())

            if verbose:
                print(f"keys for stored rates on grids are: {keys}")
            return keys


    def tex_result(self, hyperparameter, interval=0.9, verbose=True, group="posterior"):
        """
        Gives a `TeX` formated median and credible interval for a given hyperparameter.

        Parameters
        ----------
        hyperparameter: str
            Name of hyperparameter (must be in 'hyperparameters' metadata).
        interval: float, optional
            Credible interval to compute uncertainties (e.g., `interval=0.9` returns 90% credible
            intervals).
        verbose: bool
            Whether to print out result.
        group: str
            Group to compute median and credible intervals from ('posterior' or 'prior').

        Returns
        -------
        result: str
            String containing hyperparameter name, median, and plus/minus credible interval.
        """
        dataset = self.get_hyperparameter_samples(hyperparameters=hyperparameter, group=group)

        median, plus, minus = gen_credible_interval(dataset, interval, pm_format=True)

        hyperparameter_latex_labels = self.get_metadata('hyperparameter_latex_labels')
        if hyperparameter_latex_labels is not None:
            idx = np.flatnonzero(self.get_metadata('hyperparameters') == hyperparameter)[0]
            hyperparameter_label = hyperparameter_latex_labels[idx]
        else:
            hyperparameter_label = hyperparameter
        hyperparameter_label = hyperparameter_label.replace('$', '')
        fmt = '{{0:{0}}}'.format('.2f').format

        result = f'${hyperparameter_label} = {fmt(median)}^{{+{fmt(plus)}}}_{{-{fmt(minus)}}}$'

        if verbose:
            print(f"{hyperparameter} ({interval*100}% credibility): {result}")
        return result


    def _check_for_hyperparameter_sample_idx_map(self, dataset):
        """
        Checks that a `hyperparameter_sample_idx_map` has been defined.

        Parameters
        ----------
        dataset: h5py.Dataset
            Dataset to check.
        """
        if isinstance(dataset.attrs['hyperparameter_sample_idx_map'], str):
            raise Exception("a `hyperparameter_sample_idx_map` has not been defined")
            

    def _set_hyperparameter_sample_idx_map(self, dataset, hyperparameter_sample_idx_map):
        """
        Sets a `hyperparameter_sample_idx_map` for a dataset.

        Parameters
        ----------
        dataset: h5py.Dataset
            Dataset to make map for.
        hyperparameter_sample_idx_map: array
            Array of indices specifying which subset of elements in `hyperparameter_samples`
            correspond to the elements in a dataset of interest.
        """
        if hyperparameter_sample_idx_map is None:
            dataset.attrs['hyperparameter_sample_idx_map'] = 'None'
        else:
            dataset.attrs['hyperparameter_sample_idx_map'] = hyperparameter_sample_idx_map


    def _mask_with_idx(self, selections):
        """
        Creates mask using indexes.

        Parameters
        ----------
        selections: int or list of ints
            Indexes to select, `None` returns a mask including all elements in array.
        
        Returns
        -------
        mask: slice or list of ints
            Mask formatted from selections.
        """
        if selections is None:
            mask = slice(None)
        else:
            if ((not isinstance(selections, (list, np.ndarray))) and
                (not isinstance(selections, slice))):
                mask = [selections]
            else:
                mask = selections
        return mask
    

    def _mask_with_metadata(self, f, field, selections):
        """
        Creates mask by matching keys to their corresponding array entries.

        Parameters
        ----------
        f: h5py.File or h5py.Dataset
            Open popsummary file or dataset.
        field: str
            Metadata field to match selections to.
        selections: str or list of strs
            Tags to match for in metadata.
        
        Returns
        -------
        mask: slice or list of ints
            Mask formatted from selections matched to metadata.
        """
        if selections is None:
            mask = slice(None)
        else:
            if isinstance(selections, (list, np.ndarray)):
                mask = [np.flatnonzero(f.attrs[field] == selection)[0] for selection in selections]
            else:
                mask = np.flatnonzero(f.attrs[field] == selections)
        return mask

    
    def _try_overwrite(self, f, field, overwrite):
        """
        Attempts to overwrite data if required.

        Parameters
        ----------
        f: h5py.File or h5py.Dataset
            Open popsummary file or dataset.
        field: str
            Field to attempt overwriting in `f`.
        overwrite:bool
            Whether to allow the overwrite.
        """
        if field in list(f.keys()):
            if overwrite:
                del f[field]
            else:
                raise Exception(
                    f"{field} already exists, use `overwrite=True` to overwrite it")
            
    
    def _verify_input(
            self, f, key, dataset, required_size=None, parent_key=None, parent_axis=None):
        """
        Verifies a dataset meets the requirements to be stored.

        Parameters
        ----------
        f: h5py.File or h5py.Dataset
            Open popsummary file or dataset.
        field: str
            Field to attempt overwriting in `f`.
        overwrite:bool
            Whether to allow the overwrite.
        """
        if (required_size is not None) and (dataset.ndim != required_size):
            raise Exception(
                f"`{key}` should have {required_size} dimensions but has {dataset.ndim} "
                 "dimensions")
        if parent_key is not None:
            if parent_key not in f.attrs.keys():
                raise Exception(
                    f"metadata `{parent_key}` must be assigned before `{key}`")
            if (parent_axis is not None
                and dataset.shape[parent_axis] != len(f.attrs[parent_key])):
                raise Exception(
                    f"axis {parent_axis} length of `{key}` ({dataset.shape[parent_axis]}) must "
                    f"match length of metadata `{parent_key}` ({len(f.attrs[parent_key])})")
