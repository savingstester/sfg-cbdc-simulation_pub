
# --- Grundparameter ---
EINLAGEN_B2B = 323_000_000_000  # EUR, Einlagen von Unternehmen und Selbstständigen bei Sparkassen
KREDIT_B2B = 385_000_000_000    # EUR, Kreditvolumen an Unternehmen und Selbstständige
ZINSSPANNE = 0.019              # 1,9 %, laut DSGV
REFI_ZINS = 0.045               # 4,5 %, EZB Hauptrefi
EINLAGENZINS = 0.005            # angenommener Zinsaufwand für Kundeneinlagen (konservativ)

# --- UI: Eingabeparameter ---
cbdc_anteil = st.slider("CBDC-/Stablecoin-Anteil am B2B-Zahlungsverkehr (%)", 0, 50, 10)
substitutionsrate = cbdc_anteil / 100

# Anteil des Kreditverlustes, der durch Refinanzierung ersetzt wird
refi_quote = st.slider("Anteil des Kreditverlusts, den die Sparkassen durch Refinanzierung ersetzen (%)", 0, 100, 100) / 100

# --- Simulation ---
einlagen_verlust = EINLAGEN_B2B * substitutionsrate
kredit_verlust = (einlagen_verlust / EINLAGEN_B2B) * KREDIT_B2B

# Teilweise Refinanzierung
kredit_replaced = kredit_verlust * refi_quote
umsatzverlust_nicht_refi = (kredit_verlust - kredit_replaced) * ZINSSPANNE

# Mehrkosten durch Refi für den ersetzten Teil
mehrkosten_refi = kredit_replaced * (REFI_ZINS - EINLAGENZINS)

# Gesamtbelastung: entgangene Zinserträge + zusätzliche Kosten
gesamtverlust = umsatzverlust_nicht_refi + mehrkosten_refi

# --- Ergebnisse ---
st.header("Ergebnisse")
st.metric("Einlagenverlust (EUR)", f"{einlagen_verlust:,.0f}")
st.metric("Kreditvergabeverlust (EUR)", f"{kredit_verlust:,.0f}")
st.metric("Zinsertragsverlust (nicht ersetzt) (EUR)", f"{umsatzverlust_nicht_refi:,.0f}")
st.metric("Mehrkosten durch Refinanzierung (EUR)", f"{mehrkosten_refi:,.0f}")
st.metric("Gesamtbelastung (EUR)", f"{gesamtverlust:,.0f}")

# --- Visualisierung 1: Einlagenstruktur ---
st.subheader("Visualisierung: Einlagenstruktur")
fig1, ax1 = plt.subplots()
werte1 = [EINLAGEN_B2B - einlagen_verlust, einlagen_verlust]
labels1 = ['Verbleibende Einlagen', 'Verlorene Einlagen (CBDC)']
colors1 = ['green', 'red']
ax1.pie(werte1, labels=labels1, colors=colors1, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

# --- Visualisierung 2: Belastungsstruktur ---
st.subheader("Visualisierung: Struktur der Gesamtbelastung")
fig2, ax2 = plt.subplots()
werte2 = [umsatzverlust_nicht_refi, mehrkosten_refi]
labels2 = ['Zinsertragsverlust', 'Refinanzierungskosten']
colors2 = ['orange', 'purple']
ax2.bar(labels2, werte2, color=colors2)
ax2.set_ylabel("EUR")
ax2.set_title("Komponenten der Gesamtbelastung")
st.pyplot(fig2)

st.caption("\u00a9 DSGV-Modellsimulation 2024 – Quelle: DSGV, EZB, eigene Berechnungen")
