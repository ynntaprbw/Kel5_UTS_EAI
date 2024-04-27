<?php

namespace App\Http\Controllers\Api;

//import model Post
use App\Models\Tiket;

use App\Http\Controllers\Controller;

//import resource PostResource
use App\Http\Resources\TiketResource;

//import Http request
use Illuminate\Http\Request;

//import facade Validator
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\Validator;

class TiketController extends Controller
{
    /**
     * index
     *
     * @return void
     */
    public function index()
    {
        //get all posts
        $tiket = Tiket::latest()->paginate(5);

        //return collection of posts as a resource
        return new TiketResource(true, 'List Data Tiket', $tiket);
    }

    /**
     * store
     *
     * @param  mixed $request
     * @return void
     */

    public function store(Request $request)
    {
        //define validation rules
        $validator = Validator::make($request->all(), [
            'id_destinasi'        => 'required',
            'nama_pengguna'       => 'required',
            'email_pengguna'      => 'required',
            'jumlah_tiket'        => 'required',
            'total_tagihan'       => 'required',
        ]);

        //check if validation fails
        if ($validator->fails()) {
            return response()->json($validator->errors(), 422);
        }

        // //upload image
        // $image = $request->file('gambar');
        // $image->storeAs('public/posts', $image->hashName());

        //create post
        $tiket = Tiket::create([
            'id_destinasi'          => $request->id_destinasi,
            'nama_pengguna'         => $request->nama_pengguna,
            'email_pengguna'        => $request->email_pengguna,
            'jumlah_tiket'          => $request->jumlah_tiket,
            'total_tagihan'         => $request->total_tagihan,
        ]);

        //return response
        return new TiketResource(true, 'Data tiket Berhasil Ditambahkan!', $tiket);
    }

    /**
     * show
     *
     * @param  mixed $id
     * @return void
     */
    public function show($id)
    {
        //find post by ID
        $tiket = Tiket::find($id);

        //return single post as a resource
        return new TiketResource(true, 'Detail Data tiket!', $tiket);
    }

    /**
     * update
     *
     * @param  mixed $request
     * @param  mixed $id
     * @return void
     */
    public function update(Request $request, $id)
    {
        //define validation rules
        $validator = Validator::make($request->all(), [
            'id_destinasi'        => 'required',
            'nama_pengguna'       => 'required',
            'email_pengguna'      => 'required',
            'jumlah_tiket'        => 'required',
            'total_tagihan'       => 'required',
        ]);

        //check if validation fails
        if ($validator->fails()) {
            return response()->json($validator->errors(), 422);
        }

        //find post by ID
        $tiket = Tiket::find($id);

        //update post with new image
        $tiket->update([
            'id_destinasi'          => $request->id_destinasi,
            'nama_pengguna'         => $request->nama_pengguna,
            'email_pengguna'        => $request->email_pengguna,
            'jumlah_tiket'          => $request->jumlah_tiket,
            'total_tagihan'         => $request->total_tagihan,
        ]);

        //return response
        return new TiketResource(true, 'Data tiket Berhasil Diubah!', $tiket);
    }

    /**
     * destroy
     *
     * @param  mixed $id
     * @return void
     */
    public function destroy($id)
    {

        //find post by ID
        $tiket = Tiket::find($id);

        //delete image
        Storage::delete('public/posts/'.basename($tiket->image));

        //delete post
        $tiket->delete();

        //return response
        return new TiketResource(true, 'Data tiket Berhasil Dihapus!', null);
    }
}
