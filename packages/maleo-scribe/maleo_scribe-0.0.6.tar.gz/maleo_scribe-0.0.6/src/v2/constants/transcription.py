from nexo.schemas.resource import Resource, ResourceIdentifier

TRANSCRIPTION_RESOURCE = Resource(
    identifiers=[
        ResourceIdentifier(
            key="transcription", name="Transcription", slug="transcriptions"
        )
    ],
    details=None,
)
