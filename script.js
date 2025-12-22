
//index
function fungsi1(e){
    elemen = e.currentTarget;
    console.log(elemen)
    var nama = "suci";
    document.getElementById("nama").innerHTML = " " + nama;
    
}

function fungsi2(e){
    elemen = e.currentTarget;
    var nama1 = "24650093";
    document.getElementById("nama").innerHTML = "  " + nama1;
}

function hapus(){
    document.getElementById("nama").innerHTML ="";
}

//index2
function fungsi3(e){
    elemen = e.currentTarget;
    console.log(elemen)
    var nama = "Suci Ramadani";
    document.getElementById("nama").innerHTML = "nama saya adalah " + nama;
    
}

function fungsi4(e){
    elemen = e.currentTarget;
    let nama1 = "24650093";
    document.getElementById("nama2").innerHTML = "dengan NIM  " + nama1;
}

//index3
function hapus(){
    document.getElementById("nama").innerHTML ="";
    document.getElementById("nama2").innerHTML ="";
}

function fungsi5(e){
    elemen = e.currentTarget;
    elemen.style.bagroundcolor ="yellow";
    console.log(elemen)
    let nama = "suci Ramadani";
    document.getElementById("nama").innerHTML = "nama saya adalah " + nama;
    
}

function hilang(){
    document.getElementById("nama").innerHTML = "";
}

function fungsi6(e){
    elemen = e.currentTarget;
    let nama1 = "24650093";
    document.getElementById("nama").innerHTML = "dengan NIM  " + nama1;
}

function hilang(){
    document.getElementById("nama").innerHTML = "";
}

function tambah() {
      let a = parseInt(document.getElementById("nilaiA").value) || 0;
      let b = parseInt(document.getElementById("nilaiB").value) || 0;
      document.getElementById("hasil").textContent = a + b;
    }
    function kurang() {
      let a = parseInt(document.getElementById("nilaiA").value) || 0;
      let b = parseInt(document.getElementById("nilaiB").value) || 0;
      document.getElementById("hasil").textContent = a - b;
    }
    function kali() {
      let a = parseInt(document.getElementById("nilaiA").value) || 0;
      let b = parseInt(document.getElementById("nilaiB").value) || 0;
      document.getElementById("hasil").textContent = a * b;
    }
    function bagi() {
      let a = parseInt(document.getElementById("nilaiA").value) || 0;
      let b = parseInt(document.getElementById("nilaiB").value) || 0;
      document.getElementById("hasil").textContent = a / b;
    }

    function hitung(e) {
            e.preventDefault();

            let a = document.getElementById("angka1").value;
            let b = document.getElementById("angka2").value;

            let jumlah = parseInt(a) + parseInt(b);

            document.getElementById("hasil").innerHTML =
                "<p> <b>" + jumlah + "</b></p>";
        }

    let operator = "+";

        function setOperator(op) {
            operator = op;
        }

        function hitung(e) {
            e.preventDefault();

            let a = parseInt(document.getElementById("angka1").value);
            let b = parseInt(document.getElementById("angka2").value);
            let hasil = 0;

            if (operator === "+") {
                hasil = a + b;
            } else if (operator === "-") {
                hasil = a - b;
            }

            document.getElementById("hasil").innerHTML =
                "<p><b>Hasil: " + hasil + "</b></p>";
        }

function hitungc() {
    let c = document.getElementById("celcius").value;
    let f = (c * 9/5) + 32;

    document.getElementById("hasil").innerHTML = "Fahrenheit: " + f;
}


    let kurs = 15000;
    let mode = "dollar"; 
    function konversi() {
        let nilai = document.getElementById("nilai").value;

        if (nilai === "") return;

        if (mode === "dollar") {
            let rupiah = nilai * kurs;
            document.getElementById("hasil").innerHTML = "Rupiah " + rupiah;
        } else {
            let dollar = nilai / kurs;
            document.getElementById("hasil").innerHTML = "Dollar " + dollar.toFixed(0);
        }
    }

    function tukar() {
        let nilai = document.getElementById("nilai").value;
        let hasil = document.getElementById("hasil").innerText;

        if (mode === "dollar") {
        // pindah ke Rupiah
            if (hasil !== "") {
                document.getElementById("nilai").value =
                hasil.replace("Rupiah ", "");
            } else {
                document.getElementById("nilai").value = "";
            }
            mode = "rupiah";
            document.getElementById("label").innerText = "Rupiah";
            document.getElementById("hasil").innerHTML = "Dollar:";
        } else {
        // pindah ke Dollar
            if (hasil !== "") {
                document.getElementById("nilai").value =
                    hasil.replace("Dollar ", "");
            } else {
            document.getElementById("nilai").value = "";
            }
            mode = "dollar";
            document.getElementById("label").innerText = "Dollar";
            document.getElementById("hasil").innerHTML = "Rupiah:";
        }
    }

function aksiMenu() {
            // Ambil elemen menu berdasarkan ID-nya
            var m = document.getElementById("kontenMenu");

            // Cek: Jika display-nya kosong atau none, maka tampilkan
            if (m.style.display === "none") {
                m.style.display = "block";
            } else {
                // Jika sudah tampil, sembunyikan lagi
                m.style.display = "none";
            }
        }