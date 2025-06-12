
import os
import binwalk

def test_firmware_zip():
    '''
    Test: Open firmware.zip, scan for signatures
    verify that all (and only) expected signatures are detected
    '''
    expected_start = [0, 'Zip archive data, at least v1.0 to extract, name: dir655_revB_FW_203NA/']
    expected_end = [6410581, 'End of Zip archive, footer length: 22']

    input_vector_file = os.path.join(os.path.dirname(__file__),
                                     "input-vectors",
                                     "firmware.zip")

    scan_result = binwalk.scan(input_vector_file,
                               signature=True,
                               quiet=True)

    # Test number of modules used
    assert len(scan_result) == 1

    results = scan_result[0].results
    assert results[0].offset == expected_start[0]
    assert results[0].description == expected_start[1]
    assert results[-1].offset == expected_end[0]
    assert results[-1].description == expected_end[1]
