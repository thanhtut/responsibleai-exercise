from tiny_pii.pii_pipeline import PIIPipeline


def test_process(sample_text_jt):
    piepline = PIIPipeline()
    tiny_pii_output = piepline.process(sample_text_jt)

    assert tiny_pii_output.name == 1
    assert tiny_pii_output.email == 1
    assert tiny_pii_output.address == 1
    assert tiny_pii_output.nric == 1
    assert tiny_pii_output.phone == 1

    assert (
        tiny_pii_output.redacted_text
        == "Write me a response to this email: 'Dear Sir/Mdm, this is [NAME] (NRIC: [NRIC]). I am writing in to appeal for my parking offence which occurred at [ADDRESS]. Please reach me at [EMAIL] or at [PHONE]."
    )
