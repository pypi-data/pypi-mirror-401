from mendelbrot import bcftools_interpreter


def test_missense_parsing_miss(caplog):
    # no match, no reinterpretation
    assert bcftools_interpreter.process_missense('XYZ') == 'XYZ'
    assert 'No missense found in XYZ' in caplog.text

def test_missense_parsing_hit():
    assert bcftools_interpreter.process_missense('1917T>1917K') == 'p.Thr1917Lys'

def test_stop_gained_parsing_miss(caplog):
    # no match, no reinterpretation
    assert bcftools_interpreter.process_stop_gained('XYZ') == 'XYZ'
    assert 'No stop gained found in XYZ' in caplog.text

def test_stop_gained_parsing_hit():
    assert bcftools_interpreter.process_stop_gained('812L>812*') == 'p.Leu812Ter'

def test_frameshift_parsing_miss(caplog):
    # no match, no reinterpretation
    assert bcftools_interpreter.process_frameshift('XYZ') == 'XYZ'
    assert 'No frameshift found in XYZ' in caplog.text

def test_frameshift_parsing_hit():
    assert bcftools_interpreter.process_frameshift('138FELLKPPSGGLGFSVVGLRS..1972>138LSSSNLHLEALGLVLWD*') == 'p.Phe138Leufs*18'

def test_frameshift_parsing_hit2():
    assert bcftools_interpreter.process_frameshift('375VIGYECDCAAGFELIDRKTC..821>375V*') == 'p.Ile376Terfs*1'

def test_classify():
    assert bcftools_interpreter.classify_change('1917T>1917K', 'missense') == 'p.Thr1917Lys'
    assert bcftools_interpreter.classify_change('375VIGYECDCAAGFELIDRKTC..821>375V*', 'frameshift') == 'p.Ile376Terfs*1'
    assert bcftools_interpreter.classify_change('812L>812*', 'stop_gained') == 'p.Leu812Ter'

