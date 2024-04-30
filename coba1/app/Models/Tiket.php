<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Tiket extends Model
{
    protected $table = 'tiket';
    protected $primaryKey = 'id';
    protected $fillable = [
        'nama_pengguna' ,'email_pengguna', 'jumlah_tiket','total_tagihan'
    ];
}
