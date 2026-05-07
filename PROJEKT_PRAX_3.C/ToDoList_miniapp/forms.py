from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class KorculovanieForm(FlaskForm):
    nazov = StringField(
        "Koľko minút si korčuľoval?",
        validators=[DataRequired(), Length(max=100)]
    )

    ohodnot = SelectField(
        "Ohodnoť svoju jazdu od 1 po 10",
        choices=[
            ("jeden", "1. ledva som sa držal"),
            ("dva", "2. bolo to ťažké"),
            ("tri", "3. nič moc"),
            ("styri", "4. pomalý rozbeh"),
            ("pat", "5. celkom v pohode"),
            ("sest", "6. išlo to dobre"),
            ("sedem", "7. užíval/a som si to"),
            ("osem", "8. super jazda"),
            ("deved", "9. cítil/a som sa skvelo"),
            ("desat", "10. top jazda!")
        ],
        validators=[DataRequired()]
    )

    teren = SelectField(
        "Kde si korčuľoval?",
        choices=[
            ("lad", "Ľad"),
            ("inline", "Inline dráha"),
            ("park", "Park"),
            ("hala", "Športová hala"),
            ("ulica", "Ulica")
        ],
        validators=[DataRequired()]
    )

    pocasie = SelectField(
        "Aké bolo počasie?",
        choices=[
            ("slnecno", "Slnečno"),
            ("oblacno", "Oblačno"),
            ("vietor", "Veterno"),
            ("zima", "Zima"),
            ("dazd", "Dážď")
        ]
    )

    popis = TextAreaField(
        "Opíš svoju jazdu.",
        validators=[DataRequired()]
    )

    submit = SubmitField("Ulož záznam jazdy")
