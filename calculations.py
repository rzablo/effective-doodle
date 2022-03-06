# calculations

import pandas as pd
import numpy as np

from datetime import datetime


MAXDATE = "2030-01-01"


def calc_cfd(df):
    """Berechnet die Werte für das Cumulative Flow Diagram

    Args:
        `df`: Ein DataFrame mit allen Arbeitspakete mit den Terminen der Statusübergänge

    Returns:
        Ein DataFrame mit folgenden Spalten:
            `Date`:   Datum, Beginnend 1.07.2018, eine Zeile pro Woche für 200 Wochen
            `1DevReady`:   Anzahl Arbeispakete in diesem Status in dieser Woche
            `2DevWork`:    Anzahl Arbeispakete in diesem Status in dieser Woche
            `3DevFini`:    Anzahl Arbeispakete in diesem Status in dieser Woche
            `4AbnahmeBeg`: Anzahl Arbeispakete in diesem Status in dieser Woche
            `5AbnahmeFin`: Anzahl Arbeispakete in diesem Status in dieser Woche
            `6Production`: Anzahl Arbeispakete in diesem Status in dieser Woche

    """
    ts = pd.date_range("2018-07-01", freq="W", periods=200)
    ddf = pd.DataFrame(ts)
    ddf.columns = ["Date"]  # , 'Count']
    ddf["1DevReady"] = 0
    ddf["2DevWork"] = 0
    ddf["3DevFini"] = 0
    ddf["4AbnahmeBeg"] = 0
    ddf["5AbnahmeFin"] = 0
    ddf["6Production"] = 0

    for ind in ddf.index:
        theDate = pd.to_datetime(ddf["Date"][ind])

        ddf["1DevReady"][ind] = df.loc[
            (df["DevReady"] <= theDate) & (df["DevWork"] > theDate)
        ].ID.count()
        ddf["2DevWork"][ind] = df.loc[
            (df["DevWork"] <= theDate) & (df["DevFini"] > theDate)
        ].ID.count()
        ddf["3DevFini"][ind] = df.loc[
            (df["DevFini"] <= theDate) & (df["AbnahmeBeg"] > theDate)
        ].ID.count()
        ddf["4AbnahmeBeg"][ind] = df.loc[
            (df["AbnahmeBeg"] <= theDate) & (df["AbnahmeFini"] > theDate)
        ].ID.count()
        ddf["5AbnahmeFin"][ind] = df.loc[
            (df["AbnahmeFini"] <= theDate) & (df["ProduktionReady"] > theDate)
        ].ID.count()
        ddf["6Production"][ind] = df.loc[(df["ProduktionReady"] <= theDate)].ID.count()
    return ddf


def calc_leadtime(df):
    """Berechnet die Leadtime in Zeitwochen (entsprechend 7 Tagen) für jedes Arbeitspaket

    Fehlende Werte werden ignoriert und entsprechende Zeilen aus dem Ergebnis entfernt.

    Args:
        `df`: Ein DataFrame mit allen Arbeitspakete mit den Terminen der Statusübergänge

    Returns:
        Ein DataFrame mit folgenden Spalten:
            `ID`:               aus Eingangsdaten
            `Zusammenfassung`:  aus Eingangsdaten
            `DevReady`:         aus Eingangsdaten
            `ProduktionReady`:  aus Eingangsdaten
            `Leadtime`:         Berechnete Leadtime

    """
    dfx = df[["ID", "Zusammenfassung", "Teilsystem", "DevReady", "ProduktionReady"]]

    # leere Zeiten nicht mit rechnen
    dfx[dfx["DevReady"] == MAXDATE] = pd.NaT
    dfx[dfx["ProduktionReady"] == MAXDATE] = pd.NaT

    dfx["Leadtime"] = (dfx["ProduktionReady"] - dfx["DevReady"]).dt.days / 7
    return dfx.dropna()
