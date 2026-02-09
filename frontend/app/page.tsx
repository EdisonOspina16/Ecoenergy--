'use client';

import { useState } from "react";
import { useRouter } from "next/navigation";
import styles from "../styles/page.module.css";


export default function Principal() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubscribe = async () => {
    if (!email) {
      setMessage("Por favor ingresa un correo válido");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const response = await fetch("http://localhost:5000/subscribe",{
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.error || "Error al registrar el correo");
      } else {
        setMessage("¡Gracias por unirte a la comunidad! 🌱");
        setEmail("");
      }
    } catch (error) {
      setMessage("No se pudo conectar con el servidor");
    } finally {
      setLoading(false);
    }
  };
 
  return (
    <div className={styles.container}>
      {/* TopNavBar */}
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <div className={styles.logo}>
            <div className={styles.logoIcon}>
              <span className="material-symbols-outlined"></span>
            </div>
            <h2 className={styles.logoText}>EcoEnergy</h2>
          </div>
          <nav className={styles.nav}>
            <a className={styles.navLink} href="#blog">Blog</a>
            <a className={styles.navLink} href="#impacto">Impacto</a>
            <a className={styles.navLink} href="#comunidad">Comunidad</a>
            <button
             className={styles.ctaButton}
             onClick={() => router.push("/login")}
             >
              Comenzar Ahora
            </button>
          </nav>
          <button className={styles.menuButton}>
            <span className="material-symbols-outlined">menu</span>
          </button>
        </div>
      </header>

      <main className={styles.main}>
        {/* Section 1: Hero */}
        <section className={styles.hero}>
          <div className={styles.heroGrid}>
            <div className={styles.heroContent}>
              <div className={styles.badge}>
                <span className="material-symbols-outlined">bolt</span>
                Revolución Energética
              </div>
              <h1 className={styles.heroTitle}>
                Energía Inteligente para un <span className={styles.highlight}>Futuro Sostenible</span>
              </h1>
              <p className={styles.heroDescription}>
                Optimiza tu consumo con IA y reduce tu huella de carbono mientras ahorras hasta un 40% en tus facturas mensuales de forma automática.
              </p>
              <div className={styles.heroButtons}>
                <button 
                 className={styles.primaryButton}
                 onClick={() => router.push("/registro")}
                 >
                  Empezar ahora
                </button>
                <button className={styles.secondaryButton}>
                  Ver demo
                </button>
              </div>
            </div>
            <div className={styles.heroImageWrapper}>
              <div 
                className={styles.heroImage}
                style={{backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuDGnYMYmggp-jePmRMzhQvTIJjAgUfC_bWc9V_cNKoHt6X7WdzsIrZob7f_RzuIOx2tgEQTziIJUHIk9bho-fSdwv-mLhJWtqswMF9mWD_bcaZvu_3bwAZeervSxtG_JJ-R7UemWeNwZC0WgmKQsd7lC3LhCRqc8_4GfFGYPVb1fE97jf0KV0qZ9sF96ud8ZwH07AEVz_dnd1iEyUIuEG-hMA8ZapArX65PKI60P1mDnlMNoWYdIQvMQmux5OG4eB2m9VB2gBS3a7v4')"}}
              >
              </div>
              <div className={styles.savingsCard}>
                <div className={styles.savingsIcon}>
                <span className="material-symbols-outlined">trending_down</span>
                </div>
                <div>
                  <p className={styles.savingsLabel}>Ahorro Mensual</p>
                  <p className={styles.savingsValue}>-35.4%</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Section 2: Blog/How it Works */}
        <section className={styles.howItWorks} id="blog">
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionSubtitle}>Cómo funciona</h2>
            <h3 className={styles.sectionTitle}>Educación y Monitoreo Inteligente</h3>
          </div>
          <div className={styles.cardsGrid}>
            {/* Card 1 */}
            <div className={styles.card}>
              <div className={styles.cardIcon}>
                <span className="material-symbols-outlined">settings_input_component</span>
              </div>
              <h4 className={styles.cardTitle}>Instalación Ágil</h4>
              <p className={styles.cardDescription}>
                Configuración sencilla en minutos. Nuestro hardware se conecta directamente a tu panel sin necesidad de técnicos especializados.
              </p>
              <a className={styles.cardLink} href="#">
                Leer guía <span className="material-symbols-outlined">arrow_forward</span>
              </a>
            </div>

            {/* Card 2 */}
            <div className={styles.card}>
              <div className={styles.cardIcon}>
                <span className="material-symbols-outlined">psychology</span>
              </div>
              <h4 className={styles.cardTitle}>Monitoreo IA</h4>
              <p className={styles.cardDescription}>
                Nuestra IA identifica patrones de consumo ocultos y sugiere optimizaciones personalizadas para cada electrodoméstico.
              </p>
              <a className={styles.cardLink} href="#">
                Ver tecnología <span className="material-symbols-outlined">arrow_forward</span>
              </a>
            </div>

            {/* Card 3 */}
            <div className={styles.card}>
              <div className={styles.cardIcon}>
                <span className="material-symbols-outlined">energy_savings_leaf</span>
              </div>
              <h4 className={styles.cardTitle}>Ahorro Activo</h4>
              <p className={styles.cardDescription}>
                Automatiza el apagado y encendido en horas valle para reducir el costo de la factura sin sacrificar tu comodidad diaria.
              </p>
              <a className={styles.cardLink} href="#">
                Estudio de caso <span className="material-symbols-outlined">arrow_forward</span>
              </a>
            </div>
          </div>
        </section>

        {/* Section 3: Impacto Ambiental */}
        <section className={styles.impact} id="impacto">
          <div className={styles.impactGrid}>
            <div className={styles.impactContent}>
              <h2 className={styles.impactTitle}>
                Impacto Ambiental Colectivo
              </h2>
              <p className={styles.impactDescription}>
                Cada kilovatio ahorrado es una victoria para el planeta. Juntos estamos transformando el modelo energético desde el hogar.
              </p>
              <div className={styles.statsGrid}>
                <div className={styles.statCard}>
                  <span className={styles.statValue}>12.5k</span>
                  <p className={styles.statLabel}>Toneladas CO2 Evitadas</p>
                </div>
                <div className={styles.statCard}>
                  <span className={styles.statValue}>850k</span>
                  <p className={styles.statLabel}>Árboles Equivalentes</p>
                </div>
              </div>
              <div className={styles.tips}>
                <p className={styles.tipsTitle}>
                  <span className="material-symbols-outlined">tips_and_updates</span>
                  Consejos para reducir tu huella:
                </p>
                <ul className={styles.tipsList}>
                  <li className={styles.tipItem}>
                    <span className="material-symbols-outlined">check_circle</span>
                    Aprovecha la luz natural durante las horas pico de sol.
                  </li>
                  <li className={styles.tipItem}>
                    <span className="material-symbols-outlined">check_circle</span>
                    Configura tus equipos en modo Eco con nuestra app.
                  </li>
                  <li className={styles.tipItem}>
                    <span className="material-symbols-outlined">check_circle</span>
                    Desconecta dispositivos "vampiro" durante la noche.
                  </li>
                </ul>
              </div>
            </div>
            <div className={styles.efficiencyCard}>
              <div className={styles.efficiencyCardInner}>
                <div className={styles.efficiencyHeader}>
                  <h4 className={styles.efficiencyTitle}>Eficiencia del Mes</h4>
                  <span className={styles.efficiencyBadge}>+24%</span>
                </div>
                <div className={styles.progressBars}>
                  <div className={styles.progressItem}>
                    <div className={styles.progressLabel}>
                      <span>Luz</span>
                      <span>70%</span>
                    </div>
                    <div className={styles.progressBarWrapper}>
                      <div className={styles.progressBar} style={{width: '70%'}}></div>
                    </div>
                  </div>
                  <div className={styles.progressItem}>
                    <div className={styles.progressLabel}>
                      <span>Agua Caliente</span>
                      <span>45%</span>
                    </div>
                    <div className={styles.progressBarWrapper}>
                      <div className={styles.progressBar} style={{width: '45%'}}></div>
                    </div>
                  </div>
                  <div className={styles.progressItem}>
                    <div className={styles.progressLabel}>
                      <span>Climatización</span>
                      <span>88%</span>
                    </div>
                    <div className={styles.progressBarWrapper}>
                      <div className={styles.progressBar} style={{width: '88%'}}></div>
                    </div>
                  </div>
                </div>
                <div className={styles.efficiencyFooter}>
                  <p className={styles.efficiencyQuote}>"Estás ahorrando lo suficiente para alimentar 4 bombillas LED por un año"</p>
                </div>
              </div>
              <div className={styles.decorativeCircle1}></div>
              <div className={styles.decorativeCircle2}></div>
            </div>
          </div>
        </section>

        {/* Section 4: CTA Community */}
        <section className={styles.community} id="comunidad">
          <div className={styles.communityCard}>
            <div className={styles.communityPattern}></div>
            <h2 className={styles.communityTitle}>
              Únete a la Revolución Verde
            </h2>
            <p className={styles.communityDescription}>
              Muchos usuarios ya están optimizando su hogar y ayudando al planeta. Recibe consejos exclusivos y actualizaciones mensuales.
            </p>
            <div className={styles.emailForm}>
              <input
                className={styles.emailInput}
                placeholder="Tu correo electrónico"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />

              <button
                className={styles.submitButton}
                onClick={handleSubscribe}
                disabled={loading}
              >
                {loading ? "Enviando..." : "Unirse a la comunidad"}
              </button>
            </div>

            {message && (
              <p style={{ marginTop: "10px", color: "#63861d" }}>
                {message}
              </p>
            )}           
            <div className={styles.communityStats}>
              <div className={styles.avatars}>
                <div 
                  className={styles.avatar}
                  style={{backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuAU4DbmYps2PBukQWi031EOy41DuQNTuCtSChciLw4kgmO9JNXsmfptEITHKWgH1UaDlNIwoqrQ2Z6jRaL27ieChpYuCCPWLQFMo-IIDsV9FPgQWTdG6ZFKnRSVtEuIEXqQE_miFCNL7a7kt3geFnuO7Bz-0fELFBG6xYnApirguXiX5D_RsIrYfjhyRkY4RZb5zzSgPcSbO7G9YXoZ0njgjxiWFtqkcfbRdVNdiNFxn1f-I5Jq3nNeka7KPYsNtD73C2k8hQmEpUHD')"}}
                ></div>
                <div 
                  className={styles.avatar}
                  style={{backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuA6CnWNEow9wWZRnzRDmjgPvEi1PT-_iqfYtwL1jiUVutLSf6iDa8Q4_EUCDZEzNvqaqLr5-LTRQQcPQg_KgIPo_EViET8b2LjXpOiNTRkAHx81JboV5MaNQ6suWyommsODIhAyeS1xbpVoJUckYhVgtlySYkwidPQ4_LVUy7LBdFPdarbeZC6x-LXYHfIKkhO4QM9oiznWX6MtFu_8UJ7K-qytapyqhLHqSccxBF76YsmHsBWr5yylI25zWHA0sj-2SbXiXvkjbV7i')"}}
                ></div>
                <div 
                  className={styles.avatar}
                  style={{backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuC0r1POomFJqKGeayzuLny1BlwQQXOovQoY87-KXS4nz4lFDku5L8fGUQaFvSFkquIKFwNBfieCT95IW6dT_AYC42TBxx2vSbK7arCtJ3Qi-Hx9-5bWjV2mcZ_Lhx1OfN08iqxpM9LOD7QkpVy-Z4uMgWfsTWynbpVNXfsPyjKwsCcogUOn7D2xN3dgUfN-8HpRu2l46obVLELL6zgXHw1Zai_Yv-W2cZYEsiPKnpAt9hsOA8TySKNGbpCo4U0cn3ToP4FhGjWETTft')"}}
                ></div>
                <div className={styles.avatarCount}>+50k</div>
              </div>
              <p className={styles.activeUsers}>Usuarios activos este mes</p>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className={styles.footer}>
          <div className={styles.footerContent}>
            <div className={styles.footerLogo}>
              <span className="material-symbols-outlined"></span>
              <h2 className={styles.footerLogoText}>EcoEnergy</h2>
            </div>
            <div className={styles.footerLinks}>
              <a className={styles.footerLink} href="#">Privacidad</a>
              <a className={styles.footerLink} href="#">Términos</a>
              <a className={styles.footerLink} href="#">Contacto</a>
            </div>
            <div className={styles.footerSocial}>
              <a className={styles.socialButton} href="#">
                <span className="material-symbols-outlined">share</span>
              </a>
              <a className={styles.socialButton} href="#">
                <span className="material-symbols-outlined">public</span>
              </a>
            </div>
          </div>
          <div className={styles.footerBottom}>
            <p className={styles.copyright}>© 2024 EcoEnergy. Diseñando el futuro de la energía.</p>
          </div>
        </footer>
      </main>
    </div>
  );
}

