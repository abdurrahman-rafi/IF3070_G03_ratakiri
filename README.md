# Tugas Besar 1 IF3070 Dasar Inteligensi Artifisial 2026/2027.

Program mencari pengangkutan kendaraan yang optimal dengan mencari posisi dan orientasinya di deck kapal supaya total ShippingFee maksimal, tanpa overlap, tanpa keluar deck, dan tanpa melebihi kapasitas kapal. Algoritma yang dipakai: Hill-Climbing (Steepest Ascent, Stochastic, Sideways Move, Random Restart), Simulated Annealing, dan Genetic Algorithm. Program mendukung lebih dari satu kapal.

## Setup

```bash
pip install -r requirements.txt
```

## Cara Menjalankan

Jalankan dari root repository.

```bash
python -m src.main --instance data/instance_example.json --algo steepest
```

- `--algo`: `steepest`, `stochastic`, `sideways`, `restart`, `sa`, atau `ga` (default 3 run)
- `--all`: semua algoritma sekaligus, termasuk eksperimen GA
- tanpa `--algo` atau `--all`: menampilkan satu initial state random
- parameter lain: `--runs`, `--seed`, `--out`, dan parameter algoritma seperti `--max-restart`, `--initial-temp`, `--population-size`, `--iterations`

Hasil tiap run (JSON dan satu gambar berisi state awal, state akhir, serta plot) disimpan di `output/<instance>/<algoritma>/`.

## Instance

Enam instance ada di `data/`: `instance_example`, `instance_multiship`, `instance_small`, `instance_tight_space`, `instance_tight_weight`, dan `instance_multiship_hard`.

Instance custom (misalnya 4 kapal dan 40 kendaraan) bisa dibuat dengan:

```bash
python -m src.experiments.generate_instances --ships 4 --vehicles 40 --seed 1 --out data/demo.json
```

Tanpa argumen, perintah itu membuat ulang empat instance uji di `data/`.

## Pembagian Tugas

| Nama | NIM | Tugas |
|---|---|---|
| Rafi | 18224004 | model, moves, hill climbing, CLI dan visualisasi |
| Elnora | 18224125 | genetic algorithm dan eksperimen GA, full dokumen|
| Arkandhaf | 18224116 | simulated annealing, full dokumen |

## Referensi

- S. Russell dan P. Norvig, *Artificial Intelligence: A Modern Approach*, ed. ke-4, Bab 4.
- M. L. Khodra, "Beyond Classical Search: Classical vs Local Search," YouTube, 2021. https://www.youtube.com/watch?v=oGTa9kGE3P8
- M. L. Khodra, "Beyond Classical Search: State (Value, Neighbor)," YouTube, 2021. https://www.youtube.com/watch?v=_6rla37QorM
- M. L. Khodra, "Beyond Classical Search: Hill-climbing Search," YouTube, 2021. https://www.youtube.com/watch?v=L0b0CN3Fds8
- M. L. Khodra, "Beyond Classical Search: Simulated Annealing," YouTube, 2021. https://www.youtube.com/watch?v=AdhG7HnhYrk
- M. L. Khodra, "Beyond Classical Search: Genetic Algorithm," YouTube, 2021. https://www.youtube.com/watch?v=aI41TGo9J9c
- A. Lodi, S. Martello, dan M. Monaci, "Two-dimensional packing problems: A survey," *EJOR*, vol. 141, no. 2, 2002.
- OptWhiz, "How to Optimally Pack a Container | 2D Knapsack," YouTube. https://www.youtube.com/watch?v=4CfV7A_RWrw
- Computerphile, "The Knapsack Problem & Genetic Algorithms," YouTube. https://www.youtube.com/watch?v=MacVqujSXWE
- GeeksforGeeks, "Introduction to Hill Climbing in Artificial Intelligence." https://www.geeksforgeeks.org/artificial-intelligence/introduction-hill-climbing-artificial-intelligence/
- Shippeo, "ETA meaning in business: a critical metric for supply chain success." https://www.shippeo.com/resources/explore/blog-newsletter/eta-meaning-in-business-a-critical-metric-for-supply-chain-success
