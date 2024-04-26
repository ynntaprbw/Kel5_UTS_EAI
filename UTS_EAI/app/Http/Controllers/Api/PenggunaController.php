<?php

namespace App\Http\Controllers\Api;

//import model Post
use App\Models\Pengguna;

use App\Http\Controllers\Controller;

//import resource PostResource
use App\Http\Resources\PenggunaResource;

//import Http request
use Illuminate\Http\Request;

//import facade Validator
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\Validator;

class PenggunaController extends Controller
{
    /**
     * index
     *
     * @return void
     */
    public function index()
    {
        //get all posts
        $pengguna = Pengguna::latest()->paginate(5);

        //return collection of posts as a resource
        return new PenggunaResource(true, 'List Data Pengguna', $pengguna);
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
            'nama_pengguna'     => 'required',
            'email_pengguna'   => 'required',
        ]);

        //check if validation fails
        if ($validator->fails()) {
            return response()->json($validator->errors(), 422);
        }

        // //upload image
        // $image = $request->file('gambar');
        // $image->storeAs('public/posts', $image->hashName());

        //create post
        $pengguna = Pengguna::create([
            'nama_pengguna'     => $request->nama_pengguna,
            'email_pengguna'   => $request->email_pengguna,
        ]);

        //return response
        return new PenggunaResource(true, 'Data pengguna Berhasil Ditambahkan!', $pengguna);
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
        $pengguna = Pengguna::find($id);

        //return single post as a resource
        return new PenggunaResource(true, 'Detail Data pengguna!', $pengguna);
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
            'nama_pengguna'     => 'required',
            'email_pengguna'   => 'required',
        ]);

        //check if validation fails
        if ($validator->fails()) {
            return response()->json($validator->errors(), 422);
        }

        //find post by ID
        $pengguna = Pengguna::find($id);

        //check if image is not empty
        if ($request->hasFile('gambar')) {

            //upload image
            $image = $request->file('gambar');
            $image->storeAs('public/posts', $image->hashName());

            //delete old image
            Storage::delete('public/posts/' . basename($pengguna->image));

            //update post with new image
            $pengguna->update([
                'nama_pengguna'     => $request->nama_pengguna,
                'email_pengguna'   => $request->email_pengguna,
            ]);
        }

        //return response
        return new PenggunaResource(true, 'Data pengguna Berhasil Diubah!', $pengguna);
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
        $pengguna = Pengguna::find($id);

        //delete image
        Storage::delete('public/posts/'.basename($pengguna->image));

        //delete post
        $pengguna->delete();

        //return response
        return new PenggunaResource(true, 'Data pengguna Berhasil Dihapus!', null);
    }
}
