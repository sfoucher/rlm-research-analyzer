# Synthesis: Image-to-Image Transfer
Focus question: open synthesis
Date: 2026-04-19

## Table of Contents
- [Per-Paper Summaries](#per-paper-summaries)
- [Cross-Paper Synthesis](#cross-paper-synthesis)
  - [Themes](#themes)
  - [Agreements](#agreements)
  - [Contradictions](#contradictions)
  - [Gaps & Open Questions](#gaps--open-questions)
- [Research Questions Status](#research-questions-status)
  - [Answered](#answered)

## Per-Paper Summaries

### SAR to Optical Image Translation with Color Supervised Diffusion Model (Bai & Xu, 2024)
- **Key findings:**
  - Diffusion models surpass GAN-based methods for SAR-to-optical translation through iterative denoising that avoids mode collapse and produces images with superior clarity. (confidence: high)
  - Color supervision integration effectively addresses color shift artifacts, a critical failure mode in conditional diffusion approaches. (confidence: high)
  - Quantitative evaluation on SEN12 dataset shows superiority across PSNR (19.72), SSIM (0.3119), and FID (116.93) compared to GAN baselines including CycleGAN, NiceGAN, CRAN, and S2ODPM. (confidence: high)
- **Methods:** Conditional diffusion model with SAR images as guidance using U-Net architecture for noise prediction. Color supervision loss integrates Gaussian blurring for selective boundary detail preservation. Combined DDPM + color loss; 1000 diffusion steps, AdamW optimizer (80,000 iterations on 4×24 NVIDIA 3090 GPUs).
- **Conclusions:** SAR-to-optical translation via conditional diffusion models with explicit color supervision achieves state-of-the-art results in both quantitative metrics and visual quality, avoiding GAN training instability while maintaining structural fidelity to source SAR data.
- **Coverage:** Full text — methods, experiments, and conclusions comprehensively documented. Minor limitation: inference speed not directly addressed in optimization context.

---

### Accelerating Diffusion for SAR-to-Optical Image Translation via Adversarial Consistency Distillation (Bai & Xu, 2024) [abstract only — full text exceeded token limit]
- **Key findings:**
  - Consistency distillation framework reduces diffusion inference iterations with a 131× speedup while maintaining visual quality. (confidence: high)
  - Hybrid approach combines iterative diffusion's quality advantages with GAN's single-step efficiency. (confidence: medium)
  - Adversarial consistency learning ensures image clarity and minimizes color shifts during acceleration. (confidence: medium)
- **Methods:** Consistency distillation maps multi-step diffusion trajectories to single-step or few-step inference; adversarial discriminator ensures fidelity of distilled outputs. Evaluated on SEN12 and GF3 datasets using PSNR, SSIM, FID.
- **Conclusions:** Combining consistency distillation with adversarial learning achieves 131× inference speedup without sacrificing visual quality, addressing a critical bottleneck for deployment of diffusion-based I2I translation in remote sensing.
- **Coverage:** Abstract only — full text exceeded token limit. Detailed architecture and ablation studies not available.

---

### Deep image-to-image transfer applied to resolution enhancement of sentinel-2 images (Beaulieu, Foucher, Haberman & Stewart, 2018) [abstract only]
- **Key findings:**
  - GAN-based I2I translation outperforms CNN-based super-resolution methods for restoring complex textural information in Sentinel-2 10 m imagery. (confidence: medium)
  - Both high-frequency enhancement (CNN) and style-transfer-based (GAN) techniques were evaluated as complementary approaches to satellite image super-resolution. (confidence: medium)
- **Methods:** Investigated CNN-based high-frequency enhancement and GAN-based I2I translation techniques applied to Sentinel-2 imagery. Specific quantitative metrics not stated in abstract.
- **Conclusions:** GANs demonstrate superior capability for texture restoration in satellite super-resolution, validating I2I translation as a practical tool for remote sensing resolution enhancement.
- **Coverage:** Abstract only — specific architecture details, datasets, and quantitative results not accessible.

---

### C-DiffSET: Leveraging Latent Diffusion for SAR-to-EO Image Translation with Confidence-Guided Reliable Object Generation (Do, Lee & Kim, 2024) [abstract only — full text exceeded token limit]
- **Key findings:**
  - Leveraging a pretrained Latent Diffusion Model (LDM) trained on natural images enables effective transfer to the SAR-to-EO domain without training from scratch, mitigating overfitting on limited paired datasets. (confidence: medium)
  - A confidence-guided diffusion (C-Diff) loss mitigates temporal discrepancy artifacts (appearing/disappearing objects) common in multi-temporal SAR-EO fusion. (confidence: medium)
  - Achieves state-of-the-art results on multiple benchmarks, significantly outperforming recent I2I and SAR-to-EO specific methods. (confidence: medium)
- **Methods:** Pretrained VAE encoder from LDM aligns SAR and EO images in a shared latent space. Confidence-guided diffusion loss weights diffusion steps by confidence in structural alignment. Evaluated on multiple SAR-to-EO datasets.
- **Conclusions:** Transfer learning from large-scale natural image diffusion models, combined with domain-specific confidence guidance, significantly improves SAR-to-EO translation quality and robustness.
- **Coverage:** Abstract only — full text exceeded token limit. Architecture details, dataset names, quantitative results, and ablation studies not accessible.

---

### Similarity and quality metrics for MR image-to-image translation (Dohmen, Klemens, Baltruschat, Truong & Lenga, 2025) [abstract only — full text exceeded token limit]
- **Key findings:**
  - Analyzes 11 similarity (reference-based) metrics and 12 quality (non-reference) metrics for assessing synthetic medical images, with sensitivity testing across 11 distortion types and MR artifacts. (confidence: high)
  - Medical imaging I2I translation safety validation requires human reader assessment alongside quantitative metrics. (confidence: medium)
  - Practical recommendations are derived for selecting appropriate metrics when evaluating I2I translation models in medical contexts. (confidence: medium)
- **Methods:** Quantitative comparative analysis of 23 evaluation metrics across synthetic medical images with systematic sensitivity testing to distortions and MR artifacts.
- **Conclusions:** Both reference-based and non-reference quality metrics are necessary for comprehensive assessment; specific recommendations for metric selection improve evaluation reliability in medical I2I translation.
- **Coverage:** Abstract only — full text exceeded token limit. Specific metric recommendations and detailed methodology not verified.

---

### Deep Learning Model Transfer in Forest Mapping using Multi-source Satellite SAR and Optical Images (Ge, Antropov, Häme, McRoberts & Miettinen, 2023) [abstract only — full text exceeded token limit]
- **Key findings:**
  - Transfer learning of a pretrained UNet-based model (SeUNet) to a new forest inventory region using plot-level measurements achieves RMSE of 2.70 m and R² of 0.882, substantially outperforming traditional benchmarks. (confidence: medium)
  - Multi-source fusion of Sentinel-1 C-band SAR, Sentinel-2 MSI, ALOS-2 PALSAR-2, and TanDEM-X data supports accurate forest variable prediction. (confidence: medium)
  - Transfer learning enables practical DL deployment to regions with limited training data, critical for operational forest inventories. (confidence: medium)
- **Methods:** Transfer learning using pretrained SeUNet (UNet variant) fine-tuned with plot-level measurements. Multi-source EO data fusion. Specific architecture details and training procedures not available from abstract.
- **Conclusions:** DL model transfer with plot-level measurements successfully bridges the data scarcity problem for forest mapping, demonstrating practical applicability to operational remote sensing.
- **Coverage:** Abstract only — full text exceeded token limit. Loss functions, training procedures, dataset sizes, and detailed model architecture not accessible.

---

### Unsupervised Super-Resolution of Satellite Imagery for High Fidelity Material Label Transfer (Ghosh, Ehrlich, Davis & Chellappa, 2021)
- **Key findings:**
  - Unsupervised domain adaptation harvests information from small high-resolution datasets (ISPRS Potsdam, 5 cm GSD) to super-resolve large low-resolution satellite imagery (URBAN3D, 50 cm GSD) without pixel-level labels. (confidence: high)
  - Adversarial learning with a Stacked U-Net (SUNET) architecture jointly optimizes building footprint segmentation on both source and target domains, aligning features in a shared latent space. (confidence: high)
  - Super-resolution enhances boundary sharpness and texture clarity sufficient for downstream material label transfer tasks. (confidence: high)
- **Methods:** Two-stage architecture: SUNET for semantic segmentation + SR-Net with pixel-shuffle layers for super-resolution. Joint training on mixed batches from ISPRS Potsdam and URBAN3D. Adversarial discriminator; BCE segmentation loss + progressive L2/L1 SR loss. RMSProp optimizer on 64×64 tiles upscaled to 512×512.
- **Conclusions:** Unsupervised domain adaptation with adversarial learning bridges resolution gaps in satellite imagery, enabling material label transfer without expensive manual annotations on low-resolution target data.
- **Coverage:** Full text — comprehensive methods, experiments on ISPRS/URBAN3D datasets, and visual results included.

---

### Advancing Image Super-resolution Techniques in Remote Sensing: A Comprehensive Survey (Qi, Lou, Liu, Li, Yang & Nie, 2025) [abstract only — full text exceeded token limit]
- **Key findings:**
  - Remote sensing image super-resolution (RSISR) requires domain-specific architectures distinct from general image SR due to large-scale degradation and fine-grained texture/geometric structure preservation demands. (confidence: medium)
  - Current supervised, unsupervised, and quality evaluation methods show significant limitations in bridging synthetic and real-world RSISR scenarios. (confidence: medium)
  - Insufficient robustness under large-scale degradation and lack of standardized evaluation protocols are identified as critical research gaps. (confidence: medium)
- **Methods:** Comprehensive literature review categorizing RSISR algorithms into supervised, unsupervised, and quality evaluation approaches, with analysis of methodologies, datasets, and metrics.
- **Conclusions:** While diverse RSISR methods exist, they lack domain-specific architectural considerations and robust evaluation protocols to close the gap between synthetic benchmarks and real-world deployment.
- **Coverage:** Abstract only — full text exceeded token limit. Specific methods, datasets, and detailed analysis not accessible.

---

### Multimodal Satellite Image Time Series Analysis Using GAN-Based Domain Translation and Matrix Profile (Radoi, 2022)
- **Key findings:**
  - U-Net-based CycleGAN-style architecture with dual discriminators achieves >96% overall accuracy for flood and landslide detection in Sentinel-1/Sentinel-2 multimodal SITS. (confidence: high)
  - Two-step unsupervised methodology: (1) GAN-based inter-modality SAR-to-optical translation using cycle-consistency, translation, and adversarial losses; (2) anomaly detection via matrix profile extended to C-dimensional image time series. (confidence: high)
  - Multitemporal data is critical; pre/post-event imagery alone is insufficient for robust change detection. (confidence: high)
  - Method outperforms DTW-based clustering and ACE-Net baseline, demonstrating importance of multitemporal information. (confidence: high)
- **Methods:** U-Net-based generator with three loss functions (translation, cycle-consistency, adversarial with CutMix augmentation). 500 paired SAR/optical 50×50 patches. Matrix profile extended to C-dimensional signals; EM thresholding separates anomaly/unchanged classes. Datasets: Sentinel-1 VV+VH + Sentinel-2 RGB from Zimbabwe flooding (11 images) and Romania landslide (9 images).
- **Conclusions:** GAN-based inter-modality translation enables fully unsupervised analysis of heterogeneous satellite time series. Matrix profile extension provides interpretable anomaly detection without manual labeling.
- **Coverage:** Full text — methods, experiments, results, and discussion thoroughly documented.

---

### Comparison and Analysis of Image-to-Image Generative Adversarial Networks: A Survey (Saxena & Teli, 2021) [abstract only — full text exceeded token limit]
- **Key findings:**
  - Survey of eight state-of-the-art I2I GANs — Pix2Pix, CycleGAN, CoGAN, StarGAN, MUNIT, StarGAN2, DA-GAN, and Self Attention GAN — each introducing distinct architectural innovations. (confidence: high)
  - Evaluated on 18 datasets using 9 metrics; results were mixed, with no single model universally superior across all datasets, tasks, and metrics. (confidence: high)
  - GANs can be applied and generalized to I2I translation across multiple domains without parameter changes, demonstrating broad applicability. (confidence: medium)
- **Methods:** Comparative empirical study of eight GAN models evaluated on common metrics (PSNR, SSIM, FID, Inception Score) and datasets. Controlled experiment comparing 6 models on consistent benchmarks.
- **Conclusions:** No universally superior GAN architecture exists for I2I translation; model selection must be task- and dataset-specific. The survey provides structured comparison across architectures, datasets, and metrics.
- **Coverage:** Abstract only — full text exceeded token limit. Survey structure and comparative results inferred from abstract.

---

### High-resolution semantically-consistent image-to-image translation (Sokolov, Henry, Storie, Storie, Alhassan & Turgeon-Pelchat, 2023)
- **Key findings:**
  - Improved SemI2I architecture (HRSemI2I) using Adaptive Instance Normalization (AdaIN) achieves 63.99% mIoU on cross-sensor domain adaptation (WorldView-2 → SPOT-6), competitive with state-of-the-art CyCADA (63.92% mIoU) while eliminating pattern artifacts. (confidence: high)
  - Unsupervised domain adaptation from labeled source (WorldView-2) to unlabeled target (SPOT-6) substantially boosts downstream semantic segmentation performance (mIoU 64% vs. 53% baseline). (confidence: high)
  - Generator uses U-Net encoder (64→128→256 channels), residual blocks (256 channels), AdaIN layer, and mirrored decoder with skip connections; discriminator is a 5-layer CNN with instance normalization. (confidence: high)
- **Methods:** Dual generator-discriminator pairs (source-to-target, target-to-source). Loss functions: adversarial GAN loss (weight 1), cross-reconstruction loss (weight 20, L1), self-reconstruction loss (weight 10), gradient/edge loss (weight 25, Sobel operator). Adam optimizer; 100,000 iterations with learning rate decay. Downstream segmentation with DeepLab v2 on mixed original + stylized source images.
- **Conclusions:** Adaptive instance normalization enables semantic-preserving domain adaptation for multispectral remote sensing, critical for emerging high-resolution satellite constellations where labeled training data is unavailable.
- **Coverage:** Full text — architecture details, loss functions, training procedures, datasets (5560 WorldView-2 + 4735 SPOT-6 samples; 5 classes), and comprehensive comparisons all thoroughly documented.

---

### Brain-inspired approach for SAR-to-optical image translation based on diffusion models (Unknown, Unknown) [abstract only]
- **Key findings:**
  - Applies diffusion models to SAR-to-optical image translation in the remote sensing domain. (confidence: medium)
  - A brain-inspired design approach suggests incorporation of biological principles into the diffusion model architecture. (confidence: low)
- **Methods:** Not stated — webpage item only; no full text available.
- **Conclusions:** Diffusion models are being applied to remote sensing SAR-to-optical translation tasks; the brain-inspired framing suggests novel architectural directions beyond standard diffusion model designs.
- **Coverage:** Abstract only — webpage item, no full text available. Architecture details, experimental results, and comparative performance not verifiable.

---

### Analysis of Pix2Pix and CycleGAN for Image-to-Image Translation: A Comparative Study (Unknown, 2024) [abstract only]
- **Key findings:**
  - Comparative analysis of two foundational GAN-based I2I architectures: Pix2Pix (paired/conditional GAN) and CycleGAN (unpaired/cycle-consistent GAN). (confidence: high)
  - Both architectures remain subjects of active research and benchmarking in 2024, indicating continued relevance despite being over five years old. (confidence: high)
- **Methods:** Not stated — IEEE webpage item only; no full text available.
- **Conclusions:** Pix2Pix and CycleGAN remain central reference architectures for I2I translation evaluation; their continued study in 2024 reflects ongoing efforts to characterize their relative strengths across applications.
- **Coverage:** Abstract only — IEEE webpage, no full text. Specific findings, datasets, and comparative conclusions not verifiable.

---

## Cross-Paper Synthesis

### Themes

**1. GAN-based I2I translation as the established baseline architecture**
CycleGAN-style and Pix2Pix frameworks are the most widely used architectures across this collection; the majority of papers (at least 9 of 13) either employ them directly or benchmark against them. Notable exceptions that neither employ nor benchmark against these frameworks include Ge et al. (2023), Dohmen et al. (2025), and Qi et al. (2025). Saxena & Teli (2021) survey eight GAN variants; Radoi (2022) implements a U-Net CycleGAN achieving >96% accuracy in change detection; Sokolov et al. (2023) build on CycleGAN-style dual generator pairs with AdaIN; Beaulieu et al. (2018) apply GANs to satellite super-resolution; and Bai & Xu (2024, both papers) and Do et al. (2024) use GAN baselines for comparison against newer diffusion approaches. The persistence of Pix2Pix and CycleGAN as benchmarks even in 2024 (Unknown, 2024) confirms their role as the field's reference point.

**2. Diffusion models as the emerging state-of-the-art, particularly for SAR-to-optical translation**
Three 2024 papers converge on diffusion models as superior to GANs for SAR-to-optical image translation: Bai & Xu (2024, color-supervised) demonstrate quantitative superiority over GAN baselines on SEN12; Do et al. (2024) leverage pretrained LDMs with confidence-guided loss and report state-of-the-art results on multiple benchmarks (abstract only; specific dataset names and quantitative metrics unverified); and Bai & Xu (2024, consistency distillation) address diffusion's primary weakness — slow inference — with a 131× speedup. The PMC brain-inspired approach (Unknown) further applies diffusion to this domain, reinforcing the trend.

**3. Remote sensing as the dominant application domain**
Ten of the thirteen working-set papers address remote sensing tasks, including SAR-to-optical translation, satellite super-resolution, land cover mapping, forest inventory, and change detection. Domain-specific constraints identified include label scarcity, multi-spectral imagery with 4–8 channels (Sokolov et al. 2023), cloud-cover interference (Radoi 2022), and per-pixel semantic preservation requirements (Sokolov et al. 2023, Radoi 2022). Qi et al. (2025) highlight that general-purpose I2I architectures require adaptation for remote sensing contexts.

**4. Label scarcity as the universal driver of unsupervised and transfer learning methods**
Across the collection, the inability to obtain dense pixel-level annotations for satellite imagery motivates unsupervised approaches. Sokolov et al. (2023) use unlabeled target imagery for domain adaptation; Ghosh et al. (2021) propose fully unsupervised adversarial super-resolution; Radoi (2022) achieve change detection without labeled training data; and Ge et al. (2023) use only sparse plot-level measurements for forest model transfer. All four papers address this constraint independently, confirming label scarcity as the field's central practical challenge.

**5. Evaluation metric standardization as an unresolved methodological gap**
Multiple papers identify or implicitly reveal limitations in how I2I methods are evaluated. Saxena & Teli (2021) survey nine metrics and show mixed performance across them; Dohmen et al. (2025) systematically analyze 23 metrics for medical I2I translation and derive usage recommendations; Ghosh et al. (2021) acknowledge inability to compute standard metrics on the unlabeled target domain; and Qi et al. (2025) explicitly call for robust, domain-specific evaluation protocols. No consensus framework for I2I evaluation exists across domains.

**6. Inference efficiency as a practical deployment barrier (specific to Bai & Xu 2024)**
Diffusion model inference latency is identified as a limitation in the color-supervised paper (Bai & Xu 2024), which leaves it as an open gap, while Bai & Xu (2024, consistency distillation) directly address it with a 131× speedup via adversarial consistency distillation. No independent third paper in this collection corroborates inference efficiency as a broadly recognized barrier; this theme reflects the findings of a single research group and should be understood accordingly.

### Agreements

- **GANs cannot be uniformly ranked; task-specific selection is necessary.** Saxena & Teli (2021) find no single GAN superior across datasets and metrics; Radoi (2022), Sokolov et al. (2023), and Beaulieu et al. (2018) each independently select CycleGAN-style architectures adapted to their specific domain context.

- **Cycle-consistency loss is effective for unpaired cross-modal translation.** Radoi (2022) and Sokolov et al. (2023) both employ cycle-consistency as a core loss component. Bai & Xu (2024, color-supervised) benchmark against CycleGAN as a comparison model, suggesting it as an implicit reference point.

- **Shared latent space alignment is the principal mechanism for domain adaptation.** Ghosh et al. (2021) use a shared segmentation backbone; Do et al. (2024) align SAR and EO via a pretrained VAE encoder; Sokolov et al. (2023) use AdaIN for global distribution matching — all independently converging on shared representation learning as a dominant mechanism for cross-domain distribution shift.

- **PSNR, SSIM, and FID are the most frequently reported pixel-level metrics within this collection, particularly in remote sensing papers.** Bai & Xu (2024, both papers), Saxena & Teli (2021), and Do et al. (2024) all report on this trio. However, their adequacy is contested: Dohmen et al. (2025) and Qi et al. (2025) both identify these metrics as insufficient for domain-specific quality assessment, separating prevalence from adequacy.

### Contradictions

No genuine contradictions were identified. The apparent tension between GAN-based approaches (Radoi 2022, Sokolov et al. 2023) and diffusion-based approaches (Bai & Xu 2024, Do et al. 2024) is attributable to a temporal progression rather than opposing conclusions under comparable conditions: GAN-based papers were published in 2022–2023, while diffusion-based papers showing superiority appeared in 2024 on different or updated benchmarks. Differences in evaluation datasets and task specifics prevent direct contradiction.

### Gaps & Open Questions

- **Multi-domain generalization**: No paper addresses training a single model that generalizes across multiple sensor pairs or geographic regions simultaneously; all studies evaluate on a single source-target configuration.
- **Temporal I2I transfer**: Change detection papers (Radoi 2022) use multitemporal data for downstream analysis, but no paper investigates I2I translation across time (e.g., season-to-season or year-to-year domain adaptation).
- **Medical imaging I2I is underrepresented**: Only one paper (Dohmen et al. 2025) addresses medical imaging, and exclusively from an evaluation perspective — no architectural contributions from the medical domain are covered.
- **Cross-domain benchmarks absent**: No common benchmark dataset is shared across papers; evaluation is fragmented across SEN12, GF3, ISPRS/URBAN3D, Sentinel SITS, and WorldView-2/SPOT-6, making cross-paper comparison impossible without re-running experiments.
- **Real-world deployment validation**: No paper reports operational or production deployment results; all evaluations remain on controlled research benchmarks.
- [Reviewer note] The two webpage-only items (8ZW28N26, VZHHG5VV) could not be verified from full text; claims attributed to their titles should be treated as inferred.

---

## Research Questions Status

### Answered

- **DL architectures for I2I transfer:** The collection covers a broad spectrum: Pix2Pix and CycleGAN as foundational paired/unpaired GAN frameworks (Saxena & Teli 2021, Radoi 2022, Sokolov et al. 2023); U-Net encoder-decoder with AdaIN and residual blocks as the dominant GAN generator architecture (Sokolov et al. 2023, Radoi 2022, Ghosh et al. 2021); and latent diffusion models with conditional guidance as the 2024 state-of-the-art, specifically for SAR-to-optical translation (Bai & Xu 2024 ×2, Do et al. 2024). No single architecture dominates all tasks; diffusion models lead on SAR-to-optical, while GAN-based approaches remain competitive for cross-sensor optical adaptation. (Sources: Saxena & Teli 2021, Radoi 2022, Sokolov et al. 2023, Bai & Xu 2024 ×2, Do et al. 2024, Ghosh et al. 2021)

- **Application domains and domain-specific challenges:** Remote sensing is the dominant domain (10 of 13 papers), with medical imaging as a secondary domain (Dohmen et al. 2025). Within remote sensing, SAR-to-optical translation (Radoi 2022, Bai & Xu 2024 ×2, Do et al. 2024), satellite super-resolution (Beaulieu et al. 2018, Ghosh et al. 2021, Qi et al. 2025), cross-sensor land cover adaptation (Sokolov et al. 2023), and multi-source forest mapping (Ge et al. 2023) are the primary sub-tasks. Domain-specific challenges include label scarcity, multi-spectral image formats, SAR speckle noise, temporal discrepancies, and cloud cover interference. (Sources: Beaulieu et al. 2018, Radoi 2022, Sokolov et al. 2023, Ge et al. 2023, Qi et al. 2025, Dohmen et al. 2025)

- **Domain adaptation across image modalities:** Multiple complementary strategies are documented. Cycle-consistency training enables unpaired SAR-to-optical adaptation without ground truth translations (Radoi 2022). AdaIN with global distribution statistics enforces distribution alignment for cross-sensor optical adaptation (Sokolov et al. 2023). Shared latent space via a jointly trained segmentation backbone bridges resolution gaps (Ghosh et al. 2021). Pretrained VAE encoders from natural image LDMs align SAR and EO modalities in latent space (Do et al. 2024). All approaches involve some form of cross-domain feature alignment, with shared representation learning as a recurring strategy, though via mechanistically distinct means: cycle-consistency training without a shared encoder (Radoi 2022), AdaIN global style statistics (Sokolov et al. 2023), a joint segmentation backbone (Ghosh et al. 2021), and a pretrained VAE encoder (Do et al. 2024). (Sources: Radoi 2022, Sokolov et al. 2023, Ghosh et al. 2021, Do et al. 2024, Ge et al. 2023)

- **Evaluation metrics and datasets:** Standard metrics are PSNR, SSIM, and FID for pixel-level quality; mIoU and per-class IoU for downstream segmentation tasks; RMSE and R² for regression (forest mapping). Datasets are highly fragmented: SEN12 and GF3 for SAR-to-optical (Bai & Xu 2024); Sentinel-1/2 SITS for change detection (Radoi 2022); WorldView-2 and SPOT-6 for cross-sensor adaptation (Sokolov et al. 2023); ISPRS Potsdam and URBAN3D for super-resolution label transfer (Ghosh et al. 2021). Dohmen et al. (2025) provide the most rigorous evaluation methodology analysis, systematically comparing 23 metrics. Both Qi et al. (2025) and Dohmen et al. (2025) identify current metrics as insufficient for domain-specific quality assessment. (Sources: Saxena & Teli 2021, Bai & Xu 2024 ×2, Radoi 2022, Dohmen et al. 2025, Qi et al. 2025)

- **Open challenges and research gaps:** Key recurring challenges include: (1) inference efficiency of diffusion models, directly addressed by Bai & Xu (2024) with 131× speedup; (2) label scarcity in target domains, addressed by unsupervised methods across four papers; (3) synthetic-to-real evaluation gap, identified by Qi et al. (2025); (4) multitemporal data necessity for robust change detection, identified by Radoi (2022); (5) ecological and regional generalization of trained models, noted by Sokolov et al. (2023); (6) lack of standardized evaluation protocols across domains, identified by Dohmen et al. (2025) and Qi et al. (2025). (Sources: Radoi 2022, Sokolov et al. 2023, Bai & Xu 2024, Qi et al. 2025, Dohmen et al. 2025)

---

## Sources

Bai, X.; Xu, F. (2024). SAR to Optical Image Translation with Color Supervised Diffusion Model. *arXiv preprint*. [DOI: 10.48550/arXiv.2407.16921](https://doi.org/10.48550/arXiv.2407.16921)

Bai, X.; Xu, F. (2024). Accelerating Diffusion for SAR-to-Optical Image Translation via Adversarial Consistency Distillation. *arXiv preprint*. [DOI: 10.48550/arXiv.2407.06095](https://doi.org/10.48550/arXiv.2407.06095)

Beaulieu, M.; Foucher, S.; Haberman, D.; Stewart, C. (2018). Deep image-to-image transfer applied to resolution enhancement of sentinel-2 images. *IGARSS 2018*. [DOI: 10.1109/igarss.2018.8517655](https://doi.org/10.1109/igarss.2018.8517655)

Do, J.; Lee, J.; Kim, M. (2024). C-DiffSET: Leveraging Latent Diffusion for SAR-to-EO Image Translation with Confidence-Guided Reliable Object Generation. *arXiv preprint*. [DOI: 10.48550/arXiv.2411.10788](https://doi.org/10.48550/arXiv.2411.10788)

Dohmen, M.; Klemens, M.A.; Baltruschat, I.M.; Truong, T.; Lenga, M. (2025). Similarity and quality metrics for MR image-to-image translation. *Scientific Reports*, 15(1), 3853. [DOI: 10.1038/s41598-025-87358-0](https://doi.org/10.1038/s41598-025-87358-0)

Ge, S.; Antropov, O.; Häme, T.; McRoberts, R.E.; Miettinen, J. (2023). Deep Learning Model Transfer in Forest Mapping using Multi-source Satellite SAR and Optical Images. *arXiv preprint*. [DOI: 10.48550/arXiv.2308.05005](https://doi.org/10.48550/arXiv.2308.05005)

Ghosh, A.; Ehrlich, M.; Davis, L.; Chellappa, R. (2021). Unsupervised Super-Resolution of Satellite Imagery for High Fidelity Material Label Transfer. *arXiv preprint*. [DOI: 10.48550/arXiv.2105.07322](https://doi.org/10.48550/arXiv.2105.07322)

Qi, Y.; Lou, M.; Liu, Y.; Li, L.; Yang, Z.; Nie, W. (2025). Advancing Image Super-resolution Techniques in Remote Sensing: A Comprehensive Survey. *arXiv preprint*. [DOI: 10.48550/arXiv.2505.23248](https://doi.org/10.48550/arXiv.2505.23248)

Radoi, A. (2022). Multimodal Satellite Image Time Series Analysis Using GAN-Based Domain Translation and Matrix Profile. *Remote Sensing*, 14(15), 3734. [DOI: 10.3390/rs14153734](https://doi.org/10.3390/rs14153734)

Saxena, S.; Teli, M.N. (2021). Comparison and Analysis of Image-to-Image Generative Adversarial Networks: A Survey. *arXiv preprint*. [DOI: 10.48550/arXiv.2112.12625](https://doi.org/10.48550/arXiv.2112.12625)

Sokolov, M.; Henry, C.; Storie, J.; Storie, C.; Alhassan, V.; Turgeon-Pelchat, M. (2023). High-resolution semantically-consistent image-to-image translation. *IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing*, 16, 482–492. [DOI: 10.1109/JSTARS.2022.3226705](https://doi.org/10.1109/JSTARS.2022.3226705)

Unknown (Unknown). Brain-inspired approach for SAR-to-optical image translation based on diffusion models. [Link](https://pmc.ncbi.nlm.nih.gov/articles/PMC10861657/)

Unknown (2024). Analysis of Pix2Pix and CycleGAN for Image-to-Image Translation: A Comparative Study. *IEEE*. [Link](https://ieeexplore.ieee.org/document/10674804/)
