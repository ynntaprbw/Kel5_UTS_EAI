<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');

//posts
Route::apiResource('/destinasi', App\Http\Controllers\Api\DestinasiController::class);

Route::apiResource('/tiket', App\Http\Controllers\Api\TiketController::class);
