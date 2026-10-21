# Tugas Besar 1 IF3070 Dasar Inteligensi Artifisial 2026/2027.

Program mencari pengangkutan kendaraan yang optimal dengan mencari posisi dan orientasinya di deck kapal supaya total ShippingFee maksimal, tanpa overlap, tanpa keluar deck, dan tanpa melebihi kapasitas kapal. Algoritma yang dipakai: Hill-Climbing (Steepest Ascent, Stochastic, Sideways Move, Random Restart), Simulated Annealing, dan Genetic Algorithm. Multiship.

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

Hasil tiap run (JSON, gambar state awal dan akhir, serta plot) disimpan di `output/<instance>/<algoritma>/`.

### Eksperimen Simulated Annealing

```bash
python -m src.main --instance data/instance_example.json --algo sa --runs 3 --seed 945 --initial-temp 10 --stagnation-limit 50
```

`--stagnation-limit` adalah jumlah iterasi berturut-turut tanpa peningkatan nilai
solusi valid terbaik (default 50). Hasil JSON menyimpan metrik pada `extra`:

- `rejected_count`: jumlah neighbor yang ditolak.
- `stuck_count`: jumlah episode stagnasi. Satu episode dihitung saat mencapai
  batas N; iterasi berikutnya dalam episode yang sama tidak dihitung ulang.
  Peningkatan nilai terbaik mereset penghitung iterasi dan memungkinkan episode baru.
- `stagnation_iterations`: jumlah iterasi tanpa peningkatan sejak best feasible
  terakhir membaik, atau sejak awal jika belum ada perbaikan.
- `last_value`: nilai state terakhir yang dijelajahi, sedangkan `final_value`
  adalah nilai solusi valid terbaik yang dikembalikan.

Stagnasi adalah indikator operasional, bukan bukti local optimum, dan tidak
menghentikan pencarian. Suhu awal default tetap 100; contoh di atas memakai 10
secara eksplisit. Plot peluang penerimaan dibatasi pada rentang 0 sampai 1.
Hasil lama dengan `stuck_count` tanpa `rejected_count` memakai definisi penolakan.

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
