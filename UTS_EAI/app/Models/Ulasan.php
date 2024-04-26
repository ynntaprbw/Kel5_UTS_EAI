<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Ulasan extends Model
{
    protected $table = 'ulasan';
    protected $primaryKey = 'id';
    protected $fillable = [
        'id_ulasan', 'id_destinasi', 'id_pengguna' ,'judul_ulasan','ulasan', 'rating'
    ];

    public function destinasi() : BelongsTo {
        return $this->belongsTo(Destinasi::class);
    }
    public function pengguna() : BelongsTo {
        return $this->belongsTo(Pengguna::class);
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
