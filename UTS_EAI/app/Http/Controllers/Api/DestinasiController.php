<?php

namespace App\Http\Controllers\Api;

//import model Post
use App\Models\Destinasi;

use App\Http\Controllers\Controller;

//import resource PostResource
use App\Http\Resources\DestinasiResource;

//import Http request
use Illuminate\Http\Request;

//import facade Validator
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\Validator;

class DestinasiController extends Controller
{
    /**
     * index
     *
     * @return void
     */
    public function index()
    {
        //get all posts
        $destinasi = Destinasi::latest()->paginate(5);

        //return collection of posts as a resource
        return new DestinasiResource(true, 'List Data Destinasi', $destinasi);
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
            'gambar'                  => 'required|image|mimes:jpeg,png,jpg,gif,svg|max:2048',
            'nama_destinasi'          => 'required',
            'nama_penerbangan'        => 'required',
            'harga'                   => 'required',
            // 'tanggal_keberangkatan'   => 'required',
            // 'jam_keberangkatan'       => 'required',
        ]);

        //check if validation fails
        if ($validator->fails()) {
            return response()->json($validator->errors(), 422);
        }

        //upload image
        $image = $request->file('gambar');
        $image->storeAs('public/posts', $image->hashName());

        //create post
        $destinasi = Destinasi::create([
            'gambar'                  => $image->hashName(),
            'nama_destinasi'          => $request->nama_destinasi,
            'nama_penerbangan'        => $request->nama_penerbangan,
            'harga'                   => $request->harga,
            // 'tanggal_keberangkatan'   => $request->tanggal_keberangkatan,
            // 'jam_keberangkatan'       => $request->jam_keberangkatan,
        ]);

        //return response
        return new DestinasiResource(true, 'Data Destinasi Berhasil Ditambahkan!', $destinasi);
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
        $destinasi = Destinasi::find($id);

        //return single post as a resource
        return new DestinasiResource(true, 'Detail Data Destinasi!', $destinasi);
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
            'gambar'                  => 'required|image|mimes:jpeg,png,jpg,gif,svg|max:2048',
            'nama_destinasi'          => 'required',
            'nama_penerbangan'        => 'required',
            'harga'                   => 'required',
            // 'tanggal_keberangkatan'   => 'required',
            // 'jam_keberangkatan'       => 'required',
        ]);

        //check if validation fails
        if ($validator->fails()) {
            return response()->json($validator->errors(), 422);
        }

        //find post by ID
        $destinasi = Destinasi::find($id);

        //check if image is not empty
        if ($request->hasFile('gambar')) {

            //upload image
            $image = $request->file('gambar');
            $image->storeAs('public/posts', $image->hashName());

            //delete old image
            Storage::delete('public/posts/' . basename($destinasi->image));

            //update post with new image
            $destinasi->update([
                'gambar'                  => $image->hashName(),
                'nama_destinasi'          => $request->nama_destinasi,
                'nama_penerbangan'        => $request->nama_penerbangan,
                'harga'                   => $request->harga,
                'tanggal_keberangkatan'   => $request->content,
                'jam_keberangkatan'       => $request->content,
            ]);
        } else {

            //update post without image
            $destinasi->update([
                'nama_destinasi'          => $request->nama_destinasi,
                'nama_penerbangan'        => $request->nama_penerbangan,
                'harga'                   => $request->harga,
                'tanggal_keberangkatan'   => $request->content,
            ]);
        }

        //return response
        return new DestinasiResource(true, 'Data destinasi Berhasil Diubah!', $destinasi);
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
        $destinasi = Destinasi::find($id);

        //delete image
        Storage::delete('public/posts/'.basename($destinasi->image));

        //delete post
        $destinasi->delete();

        //return response
        return new DestinasiResource(true, 'Data destinasi Berhasil Dihapus!', null);
    }

}

