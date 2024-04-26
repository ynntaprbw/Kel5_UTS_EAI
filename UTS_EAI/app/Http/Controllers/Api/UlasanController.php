<?php

namespace App\Http\Controllers\Api;

//import model Post
use App\Models\Ulasan;

use App\Http\Controllers\Controller;

//import resource PostResource
use App\Http\Resources\UlasanResource;

//import Http request
use Illuminate\Http\Request;

//import facade Validator
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\Validator;

class UlasanController extends Controller
{
    /**
     * index
     *
     * @return void
     */
    public function index()
    {
        //get all posts
        $ulasan = Ulasan::latest()->paginate(5);

        //return collection of posts as a resource
        return new UlasanResource(true, 'List Data Ulasan', $ulasan);
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
            'id_destinasi'      => 'required',
            'id_pengguna'       => 'required',
            'judul_ulasan'      => 'required',
            'ulasan'            => 'required',
            'rating'            => 'required',
        ]);

        //check if validation fails
        if ($validator->fails()) {
            return response()->json($validator->errors(), 422);
        }

        // //upload image
        // $image = $request->file('gambar');
        // $image->storeAs('public/posts', $image->hashName());

        //create post
        $ulasan = Ulasan::create([
            'id_destinasi'      => $request->id_destinasi,
            'id_pengguna'       => $request->id_pengguna,
            'judul_ulasan'      => $request->judul_ulasan,
            'ulasan'            => $request->ulasan,
            'rating'            => $request->rating,
        ]);

        //return response
        return new UlasanResource(true, 'Data ulasan Berhasil Ditambahkan!', $ulasan);
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
        $ulasan = Ulasan::find($id);

        //return single post as a resource
        return new UlasanResource(true, 'Detail Data ulasan!', $ulasan);
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
            'id_destinasi'      => 'required',
            'id_pengguna'       => 'required',
            'judul_ulasan'      => 'required',
            'ulasan'            => 'required',
            'rating'            => 'required',
        ]);

        //check if validation fails
        if ($validator->fails()) {
            return response()->json($validator->errors(), 422);
        }

        //find post by ID
        $ulasan = Ulasan::find($id);

        //check if image is not empty
        if ($request->hasFile('gambar')) {

            //upload image
            $image = $request->file('gambar');
            $image->storeAs('public/posts', $image->hashName());

            //delete old image
            Storage::delete('public/posts/' . basename($ulasan->image));

            //update post with new image
            $ulasan->update([
                'id_destinasi'      => $request->id_destinasi,
                'id_pengguna'       => $request->id_pengguna,
                'judul_ulasan'      => $request->judul_ulasan,
                'ulasan'            => $request->ulasan,
                'rating'            => $request->rating,
            ]);
        }

        //return response
        return new UlasanResource(true, 'Data Ulasan Berhasil Diubah!', $ulasan);
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
        $ulasan = Ulasan::find($id);

        //delete image
        Storage::delete('public/posts/'.basename($ulasan->image));

        //delete post
        $ulasan->delete();

        //return response
        return new UlasanResource(true, 'Data Ulasan Berhasil Dihapus!', null);
    }
}
