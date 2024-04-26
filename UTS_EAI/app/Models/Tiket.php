<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Tiket extends Model
{
    protected $table = 'tiket';
    protected $primaryKey = 'id';
    protected $fillable = [
        'id_tiket', 'id_destinasi', 'id_pengguna' ,'jumlah_tiket','total_tagihan'
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
