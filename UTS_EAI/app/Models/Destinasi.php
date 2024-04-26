<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Destinasi extends Model
{
    protected $table = 'destinasi';
    protected $primaryKey = 'id';
    protected $fillable = [
        'id_destinasi', 'gambar','nama_destinasi', 'nama_penerbangan' ,'harga','tanggal_keberangkatan', 'jam_keberangkatan'
    ];

    public function tiket() : HasMany {
        return $this->hasMany(Tiket::class);
    }
    public function ulasan() : HasMany {
        return $this->hasMany(Ulasan::class);
    }

    /**
     * image
     *
     * @return Attribute
     */
    protected function image(): Attribute
    {
        return Attribute::make(
            get: fn ($image) => url('/storage/posts/' . $image),
        );
    }
}
