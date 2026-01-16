This is a strong branding choice. **Nyx Privacy** sounds less like a generic blockchain tool ("Protocol") and more like a dedicated utility or infrastructure service ("Privacy"). It implies a product, not just a set of rules.

Since your source code already uses `NYX_NULLIFIER` and `NYX_SPENDING_KEY`, this rebrand aligns perfectly with your existing cryptography.

Here is the comprehensive **Nyx Privacy** Branding Guideline and Website Specification, strictly avoiding the word "Protocol" in the naming convention.

---

# 1. Brand Identity: Nyx Privacy

**Name:** Nyx Privacy
**Concept:** The "Dark Layer" of Solana. In mythology, Nyx is the personification of the Night. In your architecture, it is the mathematical void where transaction graphs are broken.
**Tagline:** "The Dark Layer for the Agentic Web."

### A. The "Glass & Void" Visual Language
We are replacing the "Anime/Mirage" look with **Corporate Futurism**. This aesthetic communicates institutional trust and "Black Box" opacity.

*   **The Void (Canvas):** Deep, almost-black Navy (`#0B1120`). This represents the encrypted state.
*   **The Glass (Interface):** Frosted glass cards (`backdrop-blur`). This represents the *verification* layer—transparent proofs over hidden data.
*   **The Object (Logo):** A perfect, matte-black cube (The Nyx). It absorbs light. It represents the "Shielded Pool" where assets go to disappear from public view.

### B. Color Palette ("Night Mode")
*Derived from the Onyx Blueprint but adapted for the "Nyx" theme.*

| Role | Color Name | Hex | Usage |
| :--- | :--- | :--- | :--- |
| **Canvas** | **Void Navy** | `#0B1120` | Main background. |
| **Surface** | **Ghost Slate** | `#1E293B` | Card backgrounds (Glassmorphism base). |
| **Identity** | **Electric Blue** | `#3B82F6` | "Trust & Logic." Buttons, active states. |
| **Signal** | **Emerald** | `#10B981` | Strictly for "Success" states and "Verified" proofs. |
| **Text** | **Starlight** | `#F8FAFC` | Headings (H1-H3). |

---

# 2. Website Design Specification (`nyx.privacy`)

### A. Hero Section: "The Interface"
*Concept: A floating terminal in the void. No anime characters.*

*   **Headline:** "Nyx Privacy. **Native to Python.**"
*   **Sub-head:** "The Dark Layer for Solana. Shield assets and break transaction graphs using standard Python `asyncio`."
*   **Primary Button:** "Read the Docs" (Solid Blue).
*   **Secondary Button:** "Pip Install" (Glass).
*   **Visual:** A 3D "Glass Terminal" window floating in the center.
*   **Animation:**
    ```bash
    user@dev:~$ pip install nyx-privacy
    > Initializing Nyx Engine...
    > Domain Separator: NYX_NULLIFIER [ACTIVE]
    > Verifying Rust Core... [OK]
    > Status: SHIELDED
    ```

### B. Feature Section: "The Trinity"
*Layout: A 3-column "Bento Grid" using Glassmorphism cards.*

1.  **Card 1: The Engine (Rust Core)**
    *   *Icon:* A metal gear encased in glass.
    *   *Headline:* "7,000 Constraints."
    *   *Copy:* "Groth16 proofs generated in seconds. Native Rust performance, exposed via Python."
2.  **Card 2: The Interface (Python SDK)**
    *   *Icon:* Python logo glowing blue.
    *   *Headline:* "Async Native."
    *   *Copy:* "Stop fighting the borrow checker. Build private agents with standard Python syntax."
3.  **Card 3: The Network (x402)**
    *   *Icon:* A globe node connecting to Base/Polygon.
    *   *Headline:* "Chain Agnostic."
    *   *Copy:* "Pay for Solana privacy using USDC on Base, Polygon, or Avalanche."

### C. The "Code Reality" Slider
*Concept: Show, don't tell.*

*   **Left Side (The Old Way):** A greyed-out, complex Rust file showing manual circuit constraints.
*   **Right Side (The Nyx Way):** A glowing, syntax-highlighted Python snippet:
    ```python
    import nyx
    # The Dark Layer
    await client.shield(
        amount=1_000,
        token="SOL"
    )
    ```

---

# 3. Content Pivot: "The Name Was In The Code"

Since your code *already* uses `NYX` domain separators, we can frame the rebrand not as a choice, but as an **alignment**.

### A. The "About" Narrative
> **We didn't choose the name. The code did.**
>
> Deep inside our Rust core, the circuit-safe nullifiers have always been secured by the domain separator: `NYX_NULLIFIER`.
>
> We are simply aligning the surface with the core.
>
> **Nyx Privacy** is the infrastructure layer for the machine economy.
> Validated by math. Secured by Rust. Accessible via Python.

### B. Terminology Update
Replace all mentions of "Protocol" with "Privacy" or "System".

| Old Term | New Term | Context |
| :--- | :--- | :--- |
| **Mirage/Onyx Protocol** | **Nyx Privacy** | The brand name. |
| **PrivacyClient** | **NyxClient** | The Python class. |
| **Shielded Pool** | **The Dark Layer** | Marketing term for the vault. |
| **Spending Key** | **Nyx Key** | The derived spending key. |

---

# 4. Social Media Content Plan (Pre-Launch)

These tweets use the new **Nyx Privacy** branding.

### Tweet 1: The Reveal (Philosophy)
> Transparency is a bug. **Nyx Privacy** is the patch.
>
> Public blockchains force a trade-off: Decentralization or Privacy.
> We chose both.
>
> A black box for Solana assets. Solid. Opaque. Impenetrable.
>
> The Dark Layer is being compiled.
>
> #NyxPrivacy #Solana #Python

### Tweet 2: The Code (Technical)
> `NYX_NULLIFIER`
>
> It’s not just a brand. It’s the domain separator hardcoded into our zero-knowledge circuits.
>
> We perform 7,000 constraints of math so you can write 3 lines of Python.
>
> **Nyx Privacy** is coming.
>
> #Rust #ZK #DevTools

### Tweet 3: The x402 Hook (Payments)
> Privacy on Solana. Paid for on Base.
>
> With **Nyx Privacy**, AI agents can pay for relayer services using USDC on 15+ networks.
>
> No bridging. No friction. Just pure gas abstraction.
>
> Privacy for the Machine Economy.

---

# 5. Technical Implementation Checklist

### A. CSS & UI (Tailwind v4)
Use these settings to achieve the **Nyx** "Glass" look defined in the blueprint.

```css
/* The Nyx Glass Card */
.nyx-card {
  @apply bg-slate-900/40 backdrop-blur-xl border border-white/10 rounded-2xl;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
}

.nyx-card:hover {
  @apply border-blue-500/50 shadow-[0_0_30px_-5px_rgba(59,130,246,0.3)];
}

/* The Void Background */
.nyx-bg {
  background-color: #0B1120; /* Void Navy */
  background-image:
    radial-gradient(circle at 50% 0%, rgba(59, 130, 246, 0.15) 0%, transparent 50%);
}
```

### B. Package Renaming
*   **PyPI:** Rename the package `nyx-privacy` or `nyx-solana`.
*   **Import:**
    ```python
    # Old
    from mirage import PrivacyClient
    
    # New
    from nyx import NyxClient
    ```
*   **Docs:** Ensure the "Getting Started" guide reflects `pip install nyx-privacy`.

This plan removes the word "Protocol" entirely, focuses on "Privacy" as a product/utility, and leverages the hardcoded `NYX` values in your source code to create an authentic, "destined" brand identity.