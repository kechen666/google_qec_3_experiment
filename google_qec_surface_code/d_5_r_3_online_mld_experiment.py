import logging
import stim
import MLD
from config import setup_logging

if __name__ == "__main__":
    d=5
    r=3
    logging.info(f"----------------------r: {r}, d: {d}-------------------------")
    surface_code_circuit = stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        rounds=3,
        distance=5,
        after_clifford_depolarization=0.001,
        after_reset_flip_probability=0.002,
        before_measure_flip_probability=0.004,
        before_round_data_depolarization=0.003)
    
    surface_code_detector_model = surface_code_circuit.detector_error_model()
    ml_decoder = MLD.MaxLikelihoodDecoder(surface_code_detector_model, surface_code_detector_model.num_detectors)
    
    n=1
    syndrome = "1"*n + "0"*(ml_decoder.detector_number-n)

    setup_logging(environment='development', log_file_name = "speed_up_mld_d_3_r.log")
    ml_decoder.decode([syndrome])