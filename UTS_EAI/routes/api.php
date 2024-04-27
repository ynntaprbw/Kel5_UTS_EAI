<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');

//Destinasi
Route::apiResource('/destinasi', App\Http\Controllers\Api\DestinasiController::class);

//Tiket
Route::apiResource('/tiket', App\Http\Controllers\Api\TiketController::class);
